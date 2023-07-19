from collections.abc import (
    Iterator,
)
from lib.root.f091.common import (
    insecure_logging,
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


def ts_insecure_logging(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_LOGGING

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if insecure_logging(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f091.log_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
