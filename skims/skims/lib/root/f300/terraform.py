from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_attribute,
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


def _azure_app_authentication_off(graph: Graph, nid: NId) -> NId | None:
    if auth := get_argument(graph, nid, "auth_settings"):
        attr, attr_val, attr_id = get_attribute(graph, auth, "enabled")
        if not attr:
            return auth
        if attr_val.lower() == "false":
            return attr_id
    else:
        return nid
    return None


def _azure_as_client_certificates_enabled(
    graph: Graph, nid: NId
) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "client_cert_enabled")
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def tfm_azure_as_client_certificates_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_CLIENT_CERT_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_app_service" and (
                report := _azure_as_client_certificates_enabled(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f300.tfm_azure_as_client_certificates_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_app_authentication_off(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_APP_AUTH_OFF

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "azurerm_app_service",
                "azurerm_function_app",
            } and (report := _azure_app_authentication_off(graph, nid)):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f300.tfm_azure_app_authentication_off",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
