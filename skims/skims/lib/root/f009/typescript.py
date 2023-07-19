from collections.abc import (
    Iterator,
)
from lib.root.f009.common import (
    crypto_credentials,
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


def typescript_crypto_ts_credentials(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in crypto_credentials(graph, method_supplies):
            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f009.crypto_js_credentials_exposed",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_CRYPTO_CREDENTIALS,
    )
