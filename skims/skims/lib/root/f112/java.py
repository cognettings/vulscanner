from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
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


def java_sql_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_SQL_INJECTION
    danger_methods = {"addBatch", "execute", "executeQuery", "executeUpdate"}
    danger_set = {"userparameters", "userconnection"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            expr = n_attrs["expression"].split(".")
            if (
                expr[-1] in danger_methods
                or (
                    n_attrs["expression"] == "query"
                    and (obj_id := n_attrs.get("object_id"))
                    and graph.nodes[obj_id].get("symbol")
                    == "applicationJdbcTemplate"
                )
            ) and get_node_evaluation_results(
                method,
                graph,
                node,
                danger_set,
                graph_db=method_supplies.graph_db,
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.F112.user_controled_param",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
