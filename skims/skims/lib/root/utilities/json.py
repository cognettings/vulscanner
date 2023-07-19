from collections.abc import (
    Iterable,
)
from model.graph import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


def get_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> tuple[str | None, str, NId]:
    for attr_id in adj_ast(graph, object_id, label_type="Pair"):
        key, value = get_key_value(graph, attr_id)
        if key == expected_attr:
            return key, value, attr_id
    return None, "", ""


def get_key_value(graph: Graph, nid: NId) -> tuple[str, str]:
    key_id = graph.nodes[nid]["key_id"]
    key = graph.nodes[key_id]["value"]
    value_id = graph.nodes[nid]["value_id"]
    value = (
        graph.nodes[value_id]["value"]
        if graph.nodes[value_id].get("value")
        else ""
    )
    return key, value


def is_parent(graph: Graph, nid: NId, parents: Iterable[str]) -> bool:
    last_nid = nid
    for correct_parent in parents:
        parent = g.search_pred_until_type(graph, last_nid, {"Pair"})
        parent_id = parent[0] if parent != ("", "") else None
        if parent_id:
            key_id = graph.nodes[parent_id]["key_id"]
            key = graph.nodes[key_id]["value"]
            if key == correct_parent:
                last_nid = parent_id
                continue
            return False
        return False
    return True


def list_has_string(graph: Graph, nid: NId, value: str) -> bool:
    child_ids = adj_ast(graph, nid)
    for c_id in child_ids:
        curr_value = graph.nodes[c_id].get("value")
        if curr_value and curr_value == value:
            return True
    return False
