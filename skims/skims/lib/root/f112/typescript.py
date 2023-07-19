from collections.abc import (
    Iterator,
)
from lib.root.f112.common import (
    has_create_pool,
    sql_injection,
)
from lib.root.utilities.javascript import (
    file_imports_module,
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


def unsafe_sql_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_SQL_API_INJECTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        if not file_imports_module(graph, "mysql"):
            return

        danger_set = {"userconnection"}
        if has_create_pool(graph):
            danger_set = set()

        for n_id in method_supplies.selected_nodes:
            if sql_injection(graph, n_id, method, danger_set):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.F112.user_controled_param",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
