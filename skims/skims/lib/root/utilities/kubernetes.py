from model.graph import (
    Graph,
    NId,
)
from utils.graph import (
    adj_ast,
)


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


def get_pod_spec(graph: Graph, nid: NId) -> NId | None:
    if (
        check_template_integrity(graph, nid)
        and (kind := get_attribute(graph, nid, "kind"))
        and kind[1] == "Pod"
    ):
        spec, _, spec_id = get_attribute(graph, nid, "spec")
        if spec:
            return graph.nodes[spec_id]["value_id"]
    return None


def get_containers_capabilities(
    graph: Graph, sec_ctx: NId, type_cap: str
) -> list:
    cap = get_attribute(graph, sec_ctx, "capabilities")
    if cap[0]:
        cap_attrs = graph.nodes[cap[2]]["value_id"]
        specific_cap = get_attribute(graph, cap_attrs, type_cap)
        if specific_cap[0]:
            return get_list_from_node(graph, specific_cap[2])
    return []


def check_template_integrity(graph: Graph, nid: NId) -> bool:
    valid_template = get_attribute(graph, nid, "apiVersion")
    if valid_template[0]:
        return True
    return False


def check_template_integrity_for_all_nodes(
    graph: Graph, nids: list[str]
) -> bool:
    for nid in nids:
        valid_template = get_attribute(graph, nid, "apiVersion")
        if valid_template[0]:
            return True
    return False
