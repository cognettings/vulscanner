import ast
from collections.abc import (
    Iterator,
)
import ctx
from lib.sca.common import (
    DependencyType,
    format_pkg_dep,
    get_conan_dep_info,
    translate_dependencies_to_vulnerabilities,
)
from model.core import (
    MethodsEnum,
    Platform,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    MethodSupplies,
    NId,
)
import os
from utils.graph import (
    adj,
    adj_ast,
    match_ast_group_d,
)


def format_conanfile_dep(
    shard: GraphShard,
    node_id: NId,
    dep_info: str | None = None,
) -> DependencyType:
    dep_attrs = shard.graph.nodes[node_id]
    if dep_info is None:
        dep_info = dep_attrs["label_text"]
    product, version = get_conan_dep_info(dep_info)
    dep_line = dep_attrs["label_l"]
    return format_pkg_dep(
        product,
        version,
        dep_line,
        dep_line,
        dep_attrs["label_c"],
    )


def get_attr_requirements(
    shard: GraphShard,
    syntax_graph: Graph,
    attr_info: dict,
) -> Iterator[DependencyType]:
    val_id = attr_info["value_id"]
    requires_info = syntax_graph.nodes[val_id]
    if requires_info["label_type"] == "Literal":
        requires_eval = ast.literal_eval(requires_info["value"])
        if isinstance(requires_eval, str):
            yield format_conanfile_dep(shard, val_id, requires_eval)
        else:
            for require in requires_eval:
                yield format_conanfile_dep(shard, val_id, require)
    elif requires_info["label_type"] == "ArrayInitializer":
        arr_elements_ids = adj_ast(syntax_graph, val_id)
        for elem_id in arr_elements_ids:
            elem_attrs = syntax_graph.nodes[elem_id]
            if elem_attrs["label_type"] == "ArrayInitializer":
                elem_id = adj_ast(syntax_graph, elem_id)[0]
            yield format_conanfile_dep(shard, elem_id)


def get_method_requirements(
    shard: GraphShard,
    syntax_graph: Graph,
    method_id: NId,
) -> Iterator[DependencyType]:
    requirements_nodes = match_ast_group_d(
        syntax_graph, method_id, "MethodInvocation", depth=-1
    )
    for req_node in requirements_nodes:
        node_attrs = syntax_graph.nodes[req_node]
        if node_attrs["expression"] != "self.requires":
            continue
        req_args_id = syntax_graph.nodes[req_node].get("arguments_id")
        req_args = adj_ast(syntax_graph, req_args_id)
        yield format_conanfile_dep(shard, req_args[0])


def _resolve_deps(
    shard: GraphShard,
    conan_class_id: NId,
) -> Iterator[DependencyType]:
    syntax_graph = shard.syntax_graph
    class_block_id = syntax_graph.nodes[conan_class_id].get("block_id")
    class_attrs = adj_ast(syntax_graph, class_block_id)
    for attr in class_attrs:
        attr_info = syntax_graph.nodes[attr]
        if (
            attr_info["label_type"] == "VariableDeclaration"
            and attr_info["variable"] == "requires"
        ):
            yield from get_attr_requirements(shard, syntax_graph, attr_info)
        elif (
            attr_info["label_type"] == "MethodDeclaration"
            and attr_info["name"] == "requirements"
        ):
            yield from get_method_requirements(shard, syntax_graph, attr)


def conan_conanfile_py(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    path = shard.path
    if not path.endswith("conanfile.py"):
        return ()
    platform = Platform.CONAN
    method = MethodsEnum.CONAN_CONANFILE_PY
    with open(
        file=os.path.join(ctx.SKIMS_CONFIG.working_dir, path),
        encoding="latin-1",
    ) as handle:
        content: str = handle.read()
    shard_graph = shard.graph
    conan_class_id = None
    for node in method_supplies.selected_nodes:
        argumentlist_id = shard_graph.nodes[node]["label_field_superclasses"]
        argument_adj_ids = adj(shard_graph, argumentlist_id)
        for arg_id in argument_adj_ids:
            arg_attrs = shard_graph.nodes[arg_id]
            if arg_attrs["label_text"] == "ConanFile":
                conan_class_id = node
                break

    if not conan_class_id:
        return ()

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=_resolve_deps(shard, conan_class_id),
        path=path,
        platform=platform,
        method=method,
    )
