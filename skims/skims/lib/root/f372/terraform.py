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


def _azure_kv_only_accessible_over_https(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "https_only")
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def _azure_sa_insecure_transfer(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "enable_https_traffic_only"
    )
    if attr and attr_val.lower() == "false":
        return attr_id
    return None


def _elb2_uses_insecure_protocol(graph: Graph, nid: NId) -> NId | None:
    unsafe_protos = ("HTTP",)
    pro_key, pro_val, pro_id = get_attribute(graph, nid, "protocol")
    tar_key, tar_val, _ = get_attribute(graph, nid, "target_type")
    is_proto_required = tar_val != "lambda" if tar_key else False
    if is_proto_required:
        if pro_key is None:
            return nid
        if pro_val in unsafe_protos:
            return pro_id
    return None


def aux_serves_content_over_http(
    graph: Graph, nid: NId, arg: str
) -> Iterator[NId]:
    key_cond = "viewer_protocol_policy"
    if cache := get_argument(graph, nid, arg):
        attr_key, attr_val, attr_id = get_attribute(graph, cache, key_cond)
        if attr_key and attr_val == "allow-all":
            yield attr_id


def _serves_content_over_http(graph: Graph, nid: NId) -> Iterator[NId]:
    yield from aux_serves_content_over_http(
        graph, nid, "default_cache_behavior"
    )
    yield from aux_serves_content_over_http(
        graph, nid, "ordered_cache_behavior"
    )


def tfm_serves_content_over_http(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_CONTENT_HTTP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_cloudfront_distribution":
                for report in _serves_content_over_http(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f372.serves_content_over_http",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_elb2_uses_insecure_http_protocol(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_lb_target_group" and (
                report := _elb2_uses_insecure_protocol(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f372.elb2_uses_insecure_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_kv_only_accessible_over_https(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_ONLY_ACCESS_HTTPS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "azurerm_app_service",
                "azurerm_function_app",
            }:
                if report := _azure_kv_only_accessible_over_https(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f372.azure_only_accessible_over_http",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_sa_insecure_transfer(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_SA_INSEC_TRANSFER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_storage_account":
                if report := _azure_sa_insecure_transfer(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f372.tfm_azure_storage_account_insecure_transfer",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
