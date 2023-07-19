from collections.abc import (
    Iterator,
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
    get_node_evaluation_results,
)
from utils.graph import (
    adj_ast,
)


def java_insecure_authentication(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_AUTHENTICATION
    insecure_methods = {"setBasicAuth"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            expr = graph.nodes[node].get("expression")
            if expr in insecure_methods and get_node_evaluation_results(
                method, graph, node, set(), graph_db=method_supplies.graph_db
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f015.insecure_authentication",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _is_basic_auth(
    graph: Graph,
    args_ids: tuple[NId, ...],
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    if get_node_evaluation_results(
        method,
        graph,
        args_ids[0],
        {"authconfig"},
        graph_db=method_supplies.graph_db,
    ) and get_node_evaluation_results(
        method,
        graph,
        args_ids[1],
        {"basicauth"},
        graph_db=method_supplies.graph_db,
    ):
        return True
    return False


def java_basic_authentication(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_BASIC_AUTHENTICATION

    def n_ids() -> Iterator[GraphShardNode]:
        """
        Source:
        https://cheatsheetseries.owasp.org/cheatsheets/
        Web_Service_Security_Cheat_Sheet.html
        """
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs.get("expression") == "setHeader"
                and (al_id := n_attrs.get("arguments_id"))
                and (childs := adj_ast(graph, al_id))
                and len(childs) > 1
                and _is_basic_auth(graph, childs, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f015.basic_authentication",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
