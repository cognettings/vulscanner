from collections.abc import (
    Iterator,
)
from lib.root.f066.common import (
    nid_uses_console_log,
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


def ts_uses_console_log(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_USES_CONSOLE_LOG

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in nid_uses_console_log(graph, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.generic_uses_console_log",
        desc_params=dict(lang="Typescript"),
        graph_shard_nodes=n_ids(),
        method=method,
    )
