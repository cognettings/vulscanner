from collections.abc import (
    Iterable,
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MetadataGraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    get_vulnerabilities_from_n_ids_metadata,
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
from utils.string import (
    split_on_first_dot as split_fr,
)


def is_point_manager_vulnerable(
    method: MethodsEnum,
    graph: Graph,
    n_id: str,
    method_supplies: MethodSupplies,
) -> NId | None:
    member_str = (
        "Switch.System.ServiceModel."
        "DisableUsingServicePointManagerSecurityProtocols"
    )
    rules = {
        member_str,
        "true",
    }
    pred = g.pred_ast(graph, n_id)[0]
    if get_node_evaluation_results(
        method, graph, pred, rules, graph_db=method_supplies.graph_db
    ):
        return pred
    return None


def is_insecure_protocol(
    graph: Graph,
    n_id: str,
    obj_identifiers: Iterable[str],
    method_supplies: MethodSupplies,
) -> bool:
    method = MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL
    if (
        (split_expr := split_fr(graph.nodes[n_id].get("expression")))
        and split_expr[0] in obj_identifiers
        and split_expr[1] == "GetSharedAccessSignature"
        and get_node_evaluation_results(
            method, graph, n_id, set(), graph_db=method_supplies.graph_db
        )
    ):
        return True
    return False


def c_sharp_weak_protocol(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_WEAK_PROTOCOL
    weak_protocols = ["Ssl3", "Tls", "Tls11", "None"]

    def n_ids() -> Iterator[MetadataGraphShardNode]:
        metadata = {}
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            protocol = graph.nodes[node].get("member")
            if (
                graph.nodes[node].get("expression") == "SecurityProtocolType"
                and protocol in weak_protocols
            ):
                metadata["what"] = protocol
                metadata["desc_params"] = {"protocol": protocol}
                yield shard, node, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="f016.csharp_weak_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_service_point_manager_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_SERVICE_POINT_MANAGER_DISABLED
    members = {"AppContext"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("expression") in members
                and graph.nodes[node]["member"] == "SetSwitch"
                and (
                    nid := is_point_manager_vulnerable(
                        method, graph, node, method_supplies
                    )
                )
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.service_point_manager_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_insecure_shared_access_protocol(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_SHARED_ACCESS_PROTOCOL

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            obj_identifiers = get_object_identifiers(graph, {"CloudFile"})
            if is_insecure_protocol(
                graph, node, obj_identifiers, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.insecure_shared_access_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_httpclient_no_revocation_list(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_HTTPCLIENT_NO_REVOCATION_LIST

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "name"
            ) == "HttpClient" and get_node_evaluation_results(
                method, graph, node, set(), graph_db=method_supplies.graph_db
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.httpclient_no_revocation_list",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
