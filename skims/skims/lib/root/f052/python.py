from collections.abc import (
    Iterator,
)
from lib.root.utilities.python import (
    get_danger_imported_names,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def python_insecure_cipher(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_UNSAFE_CIPHER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] == "Cipher"
                and (al_id := n_attrs.get("arguments_id"))
                and (args_ids := g.adj_ast(graph, al_id))
                and len(args_ids) > 2
                and get_node_evaluation_results(
                    method, graph, al_id, {"unsafemode"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def get_vuln_nodes(
    graph: Graph,
    method_supplies: MethodSupplies,
) -> tuple[NId, ...]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool((node.get("expression") in danger_libraries))

    danger_libraries = get_danger_imported_names(graph, {"hashlib.sha1"})

    return g.filter_nodes(
        graph, method_supplies.selected_nodes, predicate_matcher
    )


def python_insec_hash_library(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_INSEC_HASH_LIBRARY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in get_vuln_nodes(graph, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def get_danger_invocations(
    graph: Graph,
    method_supplies: MethodSupplies,
) -> tuple[str, ...]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool((node.get("expression") in dang_names))

    dang_names = get_danger_imported_names(graph, {"jwt.encode"})

    return g.filter_nodes(
        graph, method_supplies.selected_nodes, predicate_matcher
    )


def eval_danger(graph: Graph, method: MethodsEnum, n_id: NId) -> bool:
    nodes = graph.nodes
    child_args = g.adj(graph, n_id)

    if len(child_args) < 3:
        return True

    for path in get_backward_paths(graph, n_id):
        if evaluation := evaluate(method, graph, path, n_id):
            if "HS256" in evaluation.triggers:
                return True
            if (
                "alg" in evaluation.triggers
                or "algorithm" in evaluation.triggers
            ):
                return False
            if nodes[child_args[2]].get("label_type") != "Literal":
                return True

    return False


def get_vuln_nodes_jwt(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for n_id in get_danger_invocations(graph, method_supplies):
        if (
            args_n_id := g.match_ast_d(graph, n_id, "ArgumentList")
        ) and eval_danger(graph, method, args_n_id):
            vuln_nodes.add(n_id)

    return vuln_nodes


def python_insec_sign_algorithm(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in get_vuln_nodes_jwt(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
