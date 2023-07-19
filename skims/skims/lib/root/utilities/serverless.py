from collections.abc import (
    Iterator,
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


def get_attr_inside_attrs(
    graph: Graph, nid: NId, attrs: list
) -> tuple[str | None, str, NId]:
    curr_nid = nid
    final_key, final_val, final_id = None, "", ""
    attr, attr_val, attr_id = None, "", ""
    for key in attrs:
        if not curr_nid:
            break
        attr, attr_val, attr_id = get_attribute(graph, curr_nid, key)
        if not attr:
            break
        curr_nid = graph.nodes[attr_id].get("value_id")
    else:
        final_key, final_val, final_id = attr, attr_val, attr_id

    return final_key, final_val, final_id


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


def _aux_iterate_events(graph: Graph, function_attrs: NId) -> Iterator[NId]:
    for c_id in adj_ast(graph, function_attrs):
        transaction_attrs = graph.nodes[c_id]["value_id"]
        events = get_attribute(graph, transaction_attrs, "events")
        if events[0]:
            event_attr = graph.nodes[events[2]]["value_id"]
            for event in adj_ast(graph, event_attr):
                yield event


def iterate_events(graph: Graph) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        functions = get_attribute(graph, nid, "functions")
        if functions[0] and functions[1] == "":
            function_attrs = graph.nodes[functions[2]]["value_id"]
            yield from _aux_iterate_events(graph, function_attrs)
