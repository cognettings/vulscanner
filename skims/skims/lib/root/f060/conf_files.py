from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    get_key_value,
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
from utils.graph import (
    adj_ast,
)


def has_insecure_flag(graph: Graph, nid: NId, key: str) -> Iterator[NId]:
    if key == "scripts":
        c_ids = adj_ast(graph, nid)
        for c_id in c_ids:
            value_id = graph.nodes[c_id]["value_id"]
            value = graph.nodes[value_id].get("value")
            if value and " --disable-host-check" in value:
                yield c_id


def allowed_hosts(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSON_ALLOWED_HOSTS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            key, value = get_key_value(graph, nid)
            if key == "AllowedHosts" and value == "*":
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.json_allowed_hosts",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def disable_host_check(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSON_DISABLE_HOST_CHECK

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            key, _ = get_key_value(graph, nid)
            value_id = graph.nodes[nid]["value_id"]
            result = has_insecure_flag(graph, value_id, key)
            for vuln in result:
                yield shard, vuln

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f060.json_disable_host_check",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
