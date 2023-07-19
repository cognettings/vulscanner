from collections.abc import (
    Iterator,
)
from lib.root.f280.common import (
    has_dangerous_param,
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


def ts_non_secure_construction(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_NON_SECURE_CONSTRUCTION_OF_COOKIES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if has_dangerous_param(method, graph, n_id):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f280.non_secure_construction_of_cookies",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
