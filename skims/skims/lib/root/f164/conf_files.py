from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    get_key_value,
    is_parent,
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


def ssl_port_missing(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSON_SSL_PORT_MISSING
    correct_parents = ["iisExpress", "iisSettings"]

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key, value = get_key_value(graph, nid)
            if (
                key == "sslPort"
                and value == "0"
                and is_parent(graph, nid, correct_parents)
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f164.json_ssl_port_missing",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
