from collections.abc import (
    Iterator,
)
from lib.root.utilities.common import (
    check_methods_expression,
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
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_sql_injection(
    graph: Graph,
    n_id: str,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    if (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (args_ids := g.adj_ast(graph, al_id))
        and len(args_ids) > 0
        and get_node_evaluation_results(
            method,
            graph,
            args_ids[0],
            set(),
            graph_db=method_supplies.graph_db,
        )
    ):
        return True
    return False


def is_execute_danger(
    graph: Graph,
    n_id: str,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    danger_methods = {
        "ExecuteNonQuery",
        "ExecuteScalar",
        "ExecuteOracleNonQuery",
        "ExecuteOracleScalar",
        "ExecuteNonQueryAsync",
        "ExecuteScalarAsync",
        "ExecuteReaderAsync",
    }
    danger_set = {"UserParams"}
    if (
        graph.nodes[n_id].get("member") in danger_methods
        and (test_id := graph.nodes[n_id].get("expression_id"))
        and get_node_evaluation_results(
            method,
            graph,
            test_id,
            danger_set,
            False,
            graph_db=method_supplies.graph_db,
        )
    ):
        return True
    return False


def c_sharp_sql_injection_execution(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_SQL_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if check_methods_expression(
                graph, node, {"ExecuteSqlCommand"}
            ) and is_sql_injection(graph, node, method, method_supplies):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.001.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_sql_injection_object(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    danger_objects = {"SqlCommand"}
    method = MethodsEnum.CS_SQL_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "name"
            ) in danger_objects and is_sql_injection(
                graph, node, method, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.001.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_sql_user_params(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_UNSAFE_SQL_STATEMENT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if is_execute_danger(graph, node, method, method_supplies):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f001.user_controled_param",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
