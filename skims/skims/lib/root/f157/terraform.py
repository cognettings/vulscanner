from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_optional_attribute,
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


def _aws_acl_broad_network_access(graph: Graph, nid: NId) -> NId | None:
    if (
        (ingress := get_argument(graph, nid, "ingress"))
        and (attr := get_optional_attribute(graph, ingress, "cidr_block"))
        and attr[1] in {"::/0", "0.0.0.0/0"}
    ):
        return attr[2]
    return None


def _aux_azure_sa_default_network_access(graph: Graph, nid: NId) -> NId | None:
    if not (attr := get_optional_attribute(graph, nid, "default_action")):
        return nid
    if attr[1].lower() != "deny":
        return attr[2]
    return None


def _azure_sa_default_network_access(graph: Graph, nid: NId) -> NId | None:
    if graph.nodes[nid].get("name") == "azurerm_storage_account_network_rules":
        return _aux_azure_sa_default_network_access(graph, nid)

    for c_id in adj_ast(graph, nid, name="network_rules"):
        return _aux_azure_sa_default_network_access(graph, c_id)
    return None


def _azure_kv_danger_bypass(graph: Graph, nid: NId) -> NId | None:
    if network := get_argument(graph, nid, "network_acls"):
        bypass = get_optional_attribute(graph, network, "bypass")
        if not bypass:
            return nid
        if bypass[1].lower() != "azureservices":
            return bypass[2]
    return None


def _azure_kv_default_network_access(graph: Graph, nid: NId) -> NId | None:
    if network := get_argument(graph, nid, "network_acls"):
        attr = get_optional_attribute(graph, network, "default_action")
        if not attr:
            return nid
        if attr[1].lower() != "deny":
            return attr[2]
    return None


def _azure_unrestricted_access_network_segments(
    graph: Graph, nid: NId
) -> NId | None:
    attr = get_optional_attribute(graph, nid, "public_network_enabled")
    if not attr:
        return nid
    if attr[1].lower() == "true":
        return attr[2]
    return None


def tfm_aws_acl_broad_network_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_ACL_BROAD_NETWORK_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_default_network_acl" and (
                report := _aws_acl_broad_network_access(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f157.aws_acl_broad_network_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_kv_danger_bypass(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_DANGER_BYPASS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_key_vault" and (
                report := _azure_kv_danger_bypass(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f157.tfm_azure_kv_danger_bypass",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_kv_default_network_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_DEFAULT_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_key_vault" and (
                report := _azure_kv_default_network_access(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f157.tfm_azure_kv_default_network_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_unrestricted_access_network_segments(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_UNRESTRICTED_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_data_factory" and (
                report := _azure_unrestricted_access_network_segments(
                    graph, nid
                )
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f157.tfm_azure_public_network_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_sa_default_network_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_SA_DEFAULT_ACCESS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "azurerm_storage_account_network_rules",
                "azurerm_storage_account",
            } and (report := _azure_sa_default_network_access(graph, nid)):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f157.tfm_azure_sa_default_network_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
