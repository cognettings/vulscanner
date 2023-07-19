from collections.abc import (
    Iterator,
)
from lib.root.f034.common import (
    weak_random,
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


def javascript_weak_random(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_WEAK_RANDOM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in weak_random(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f034.use_insecure_random_method",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
