from collections.abc import (
    Iterator,
)
from lib.root.f143.common import (
    has_eval,
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


def ts_uses_eval(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_USES_EVAL

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if has_eval(method, graph, n_id):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f143.uses_eval",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
