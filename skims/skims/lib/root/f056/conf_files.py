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
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def is_in_path(graph: Graph, nid: NId, key_pair: str, value: str) -> bool:
    correct_parents = ["iisSettings"]
    if (
        key_pair == "anonymousAuthentication"
        and value == "true"
        and is_parent(graph, nid, correct_parents)
    ):
        return True
    return False


def anon_connection_config(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSON_ANON_CONNECTION_CONFIG

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            key, value = get_key_value(graph, nid)

            if is_in_path(graph, nid, key, value):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f056.json_anon_connection_config",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
