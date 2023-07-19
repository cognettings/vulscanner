from collections.abc import (
    Iterable,
    Iterator,
)
from lib.root.utilities.c_sharp import (
    get_first_member_syntax_graph,
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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def is_type_handle_dangerous(
    method: MethodsEnum,
    graph: Graph,
    member: NId,
    obj_names: Iterable[str],
    method_supplies: MethodSupplies,
) -> bool:
    if (
        graph.nodes[member].get("member") == "TypeNameHandling"
        and (fr_memb := get_first_member_syntax_graph(graph, member))
        and graph.nodes[fr_memb].get("symbol") in obj_names
        and (pred := g.pred_ast(graph, member)[0])
        and (assign_id := g.match_ast(graph, pred)["__1__"])
    ):
        return get_node_evaluation_results(
            method, graph, assign_id, set(), graph_db=method_supplies.graph_db
        )
    return False


# https://docs.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
def c_sharp_insecure_deserialization(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_DESERIAL
    danger_objects = {
        "BinaryFormatter",
        "SoapFormatter",
        "NetDataContractSerializer",
        "LosFormatter",
        "ObjectStateFormatter",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") in danger_objects:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.096.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_check_xml_serializer(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_XML_SERIAL
    danger_set = {"Type.GetType", "HttpRequest"}
    danger_objects = {"XmlSerializer"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "name"
            ) in danger_objects and get_node_evaluation_results(
                method,
                graph,
                node,
                danger_set,
                graph_db=method_supplies.graph_db,
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.insecure_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_js_deserialization(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_JS_DESERIALIZATION
    serializer = {"JavaScriptSerializer"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "name"
            ) in serializer and get_node_evaluation_results(
                method, graph, node, set(), graph_db=method_supplies.graph_db
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.js_deserialization",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_type_name_handling(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_TYPE_NAME_HANDLING
    serializer = {"JsonSerializerSettings"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        serial_objs = get_object_identifiers(graph, serializer)
        for node in method_supplies.selected_nodes:
            if is_type_handle_dangerous(
                method, graph, node, serial_objs, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f096.type_name_handling",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
