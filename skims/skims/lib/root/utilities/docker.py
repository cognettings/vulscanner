from collections.abc import (
    Iterator,
)
from model.graph import (
    Graph,
    MethodSupplies,
    NId,
)
from utils import (
    graph as g,
)
from utils.graph import (
    adj_ast,
)


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


def validate_path(path: str) -> bool:
    last_slash_index = path.rfind("/")
    filename = path[last_slash_index:]
    if "docker" in filename.lower():
        return True
    return False


def iterate_services(graph: Graph) -> Iterator[NId]:
    for nid in g.matching_nodes(graph, label_type="Object"):
        serv, _, serv_id = get_attribute(graph, nid, "services")
        if serv:
            for c_id in adj_ast(graph, graph.nodes[serv_id]["value_id"]):
                yield c_id


def iterate_services_obj(
    graph: Graph, method_supplies: MethodSupplies
) -> Iterator[NId]:
    for nid in method_supplies.selected_nodes:
        serv, _, serv_id = get_attribute(graph, nid, "services")
        if serv:
            for c_id in adj_ast(graph, graph.nodes[serv_id]["value_id"]):
                yield c_id


def iterate_env_variables(
    graph: Graph, method_supplies: MethodSupplies
) -> Iterator[NId]:
    for nid in iterate_services_obj(graph, method_supplies):
        props = graph.nodes[nid]["value_id"]
        env = get_attribute(graph, props, "environment")
        if env[0]:
            env_variables = graph.nodes[env[2]]["value_id"]
            if graph.nodes[env_variables]["label_type"] == "ArrayInitializer":
                for var in adj_ast(graph, env_variables):
                    yield var
            else:
                yield env_variables
