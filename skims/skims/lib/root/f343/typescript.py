from collections.abc import (
    Iterator,
)
from lib.root.f343.common import (
    webpack_insecure_compression,
)
from lib.root.utilities.javascript import (
    get_default_alias,
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


def ts_insecure_compression(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.TS_INSECURE_COMPRESSION_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        if not (
            danger_library := get_default_alias(
                graph, "compression-webpack-plugin"
            )
        ):
            return

        for n_id in method_supplies.selected_nodes:
            if v_id := webpack_insecure_compression(
                graph, danger_library, n_id, method
            ):
                yield shard, v_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f343.insecure_compression_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_INSECURE_COMPRESSION_ALGORITHM,
    )
