from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    get_key_value,
    is_parent,
    list_has_string,
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
from utils import (
    graph as g,
)


def has_wildcard(graph: Graph, nid: NId) -> bool:
    parents_paths = [
        ["CorsRules", "CorsConfiguration", "Properties"],
        ["Cors", "Properties"],
        ["cors", "http"],
    ]

    if not any(is_parent(graph, nid, path) for path in parents_paths):
        return False

    value_id = graph.nodes[nid]["value_id"]

    if (
        graph.nodes[value_id]["label_type"] == "Literal"
        and graph.nodes[value_id]["value"] in {"*", "'*'"}
    ) or (
        graph.nodes[value_id]["label_type"] == "ArrayInitializer"
        and list_has_string(graph, value_id, "*")
    ):
        return True

    return False


def cfn_wildcard_in_allowed_origins(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_WILDCARD_IN_ALLOWED_ORIGINS
    danger_keys = {"allowedorigins", "alloworigin", "origin"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key_id = graph.nodes[nid]["key_id"]
            key = graph.nodes[key_id]["value"]
            if key.lower() in danger_keys and has_wildcard(graph, nid):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.wildcard_in_allowed_origins",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def is_in_path(graph: Graph, nid: NId, key_dict: str, value: str) -> bool:
    last_nid = nid
    if key_dict == "cors" and value == "true":
        parent = g.search_pred_until_type(graph, last_nid, {"Pair"})
        if parent_id := parent[0] if parent != ("", "") else None:
            key, _ = get_key_value(graph, parent_id)
            if key == "http":
                return True
    return False


def cfn_cors_true(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.YML_SERVERLESS_CORS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key, value = get_key_value(graph, nid)
            if is_in_path(graph, nid, key, value):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.wildcard_in_allowed_origins",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
