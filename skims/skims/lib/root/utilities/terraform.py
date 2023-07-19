from collections.abc import (
    Iterator,
)
from contextlib import (
    suppress,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from model.graph import (
    Graph,
    NId,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)


def is_cidr(cidr: str) -> bool:
    """Validate if a string is a valid CIDR."""
    result = False
    with suppress(AddressValueError, ValueError):
        IPv4Network(cidr, strict=False)
        result = True
    with suppress(AddressValueError, ValueError):
        IPv6Network(cidr, strict=False)
        result = True
    return result


def get_list_from_node(graph: Graph, nid: NId | None) -> list:
    if nid:
        value_id = graph.nodes[nid]["value_id"]
        if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
            child_ids = adj_ast(graph, value_id)
            result: list = []
            for c_id in child_ids:
                result.append(graph.nodes[c_id].get("value"))
            return result
        return [graph.nodes[value_id].get("value")]
    return []


def get_argument(graph: Graph, nid: NId, expected_resource: str) -> NId | None:
    for block_id in adj_ast(graph, nid, label_type="Object"):
        if graph.nodes[block_id].get("name") == expected_resource:
            return block_id
    return None


def iter_statements_from_policy_document(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for block_id in adj_ast(graph, nid, label_type="Object"):
        if graph.nodes[block_id].get("name") == "statement":
            yield block_id


def get_key_value(graph: Graph, nid: NId) -> tuple[str, str]:
    key_id = graph.nodes[nid]["key_id"]
    key = graph.nodes[key_id]["value"]
    value_id = graph.nodes[nid]["value_id"]
    value = ""
    if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
        child_id = adj_ast(graph, value_id, label_type="Literal")
        if len(child_id) > 0:
            value = graph.nodes[child_id[0]].get("value", "")
    else:
        value = graph.nodes[value_id].get("value", "")
    return key, value


def get_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> tuple[str | None, str, NId]:
    if object_id != "":
        for attr_id in adj_ast(graph, object_id, label_type="Pair"):
            key, value = get_key_value(graph, attr_id)
            if key == expected_attr:
                return key, value, attr_id
    return None, "", ""


def get_optional_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> tuple[str, str, NId] | None:
    """
    Search an optional attribute in an object node and, if found,
    return a tuple with [key_name, key_value, Node_Id]
    """
    for n_id in match_ast_group_d(graph, object_id, "Pair"):
        key, value = get_key_value(graph, n_id)
        if key == expected_attr:
            return key, value, n_id
    return None


def get_attr_inside_attrs(
    graph: Graph, nid: NId, attrs: list
) -> tuple[str, str, NId] | None:
    curr_nid = nid
    attr = None
    for key in attrs:
        if curr_nid and (attr := get_optional_attribute(graph, curr_nid, key)):
            curr_nid = graph.nodes[attr[2]].get("value_id")
    return attr


def list_has_string(graph: Graph, nid: NId, value: str) -> bool:
    child_ids = adj_ast(graph, nid)
    for c_id in child_ids:
        curr_value = graph.nodes[c_id].get("value")
        if curr_value and curr_value == value:
            return True
    return False
