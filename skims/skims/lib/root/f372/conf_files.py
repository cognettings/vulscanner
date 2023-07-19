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


def _insecure_http_server(graph: Graph, nid: NId, key: str) -> Iterator[NId]:
    required_flags = {" -S", " --tls", " --ssl"}
    if key == "scripts":
        for c_id in adj_ast(graph, nid):
            value_id = graph.nodes[c_id]["value_id"]
            value = graph.nodes[value_id].get("value")
            if (
                value
                and "http-server" in value
                and not any(flag in value for flag in required_flags)
            ):
                yield c_id


def https_flag_missing(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSON_HTTPS_FLAG_MISSING

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key, _ = get_key_value(graph, nid)
            value_id = graph.nodes[nid]["value_id"]
            for vuln_id in _insecure_http_server(graph, value_id, key):
                yield shard, vuln_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f372.json_https_flag_missing",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
