from lib.root.utilities.javascript import (
    get_default_alias,
)
from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def get_dang_instances_names_method(
    graph: Graph, dang_classes: set[str]
) -> set[str]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        nodes = graph.nodes
        return bool(
            node.get("label_type") == "VariableDeclaration"
            and (val_n_id := node.get("value_id"))
            and (
                (
                    (nodes[val_n_id].get("label_type") == "ObjectCreation")
                    and (nodes[val_n_id].get("name") in dang_classes)
                )
                or (
                    (nodes[val_n_id].get("label_type") == "MethodInvocation")
                    and (expr := nodes[val_n_id].get("expression"))
                    and (expr.split(".")[0] in dang_classes)
                )
            )
        )

    dang_names: set[str] = set()
    for n_id in g.filter_nodes(graph, graph.nodes, predicate_matcher):
        dang_names.add(graph.nodes[n_id].get("variable"))
    return dang_names


def get_danger_invocations_method(graph: Graph) -> set[str]:
    dang_methods: set[str] = {"setRequestHeader", "append", "set"}
    dang_objects = get_dang_instances_names_method(
        graph, {"XMLHttpRequest", "Headers"}
    )
    dang_imported_classes = {"superagent"}

    for dang_class in dang_imported_classes:
        if imported_alias := get_default_alias(graph, dang_class):
            dang_objects.add(imported_alias)

    danger_invocations = {
        f"{dang_name}.{dang_method}"
        for dang_name in dang_objects
        for dang_method in dang_methods
    }

    return danger_invocations


def get_dang_instances_names_object(graph: Graph) -> set[str]:
    dang_libraries: set[str] = {"axios", "ky"}
    dang_aliases: set[str] = {"fetch", "$"}

    for lib in dang_libraries:
        if dang_alias := get_default_alias(graph, lib):
            dang_aliases.add(dang_alias)
    return dang_aliases


def get_accept_header_vulns_method_1(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
) -> bool:
    danger_invocations = get_danger_invocations_method(graph)
    if (
        graph.nodes[n_id].get("expression") in danger_invocations
        and (args_n_id := graph.nodes[n_id].get("arguments_id"))
        and get_node_evaluation_results(
            method, graph, args_n_id, {"accept", "*/*"}, False
        )
    ):
        return True
    return False


def get_accept_header_vulns_method_2(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> bool:
    dang_instances = get_dang_instances_names_object(graph)
    if (
        (expr := graph.nodes[n_id].get("expression"))
        and expr.split(".")[0] in dang_instances
        and (args_n_id := graph.nodes[n_id].get("arguments_id"))
        and (args := g.adj_ast(graph, args_n_id))
    ):
        dang_types = {"Object", "SymbolLookup"}
        for susp_id in filter(
            lambda x: graph.nodes[x].get("label_type") in dang_types, args
        ):
            if get_node_evaluation_results(
                method, graph, susp_id, {"accept", "*/*"}, False
            ):
                return True
    return False


def get_accept_header_vulns_default(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> bool:
    dang_members = {
        "defaults",
        "headers",
        "common",
        "get",
        "post",
        "put",
        "patch",
        "delete",
    }

    if library_alias := get_default_alias(graph, "axios"):
        dang_members.add(library_alias)
        if library_instances := get_dang_instances_names_method(
            graph, {library_alias}
        ):
            for dang_instance in library_instances:
                dang_members.add(dang_instance)

    expr_id = graph.nodes[n_id].get("expression_id")
    if not expr_id or graph.nodes[expr_id].get("label_type") != "MemberAccess":
        return False

    if (
        (members := set(graph.nodes[expr_id].get("member").split(".")))
        and members.issubset(dang_members)
        and (arg_n_id := graph.nodes[n_id].get("arguments_id"))
        and (graph.nodes[arg_n_id].get("value")[1:-1] == "Accept")
    ):
        p_id = g.pred_ast(graph, n_id)[0]
        if graph.nodes[p_id].get(
            "label_type"
        ) == "Assignment" and get_node_evaluation_results(
            method, graph, p_id, {"*/*"}, False
        ):
            return True
    return False
