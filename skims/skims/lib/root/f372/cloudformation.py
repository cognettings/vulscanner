from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
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


def _aux_serves_content_over_http(
    graph: Graph, dist_config_id: NId
) -> Iterator[NId]:
    config_attrs = graph.nodes[dist_config_id]["value_id"]
    if (
        (
            def_cache := get_optional_attribute(
                graph, config_attrs, "DefaultCacheBehavior"
            )
        )
        and (dcb_attrs := graph.nodes[def_cache[2]]["value_id"])
        and (
            viewer_p := get_optional_attribute(
                graph, dcb_attrs, "ViewerProtocolPolicy"
            )
        )
        and viewer_p[1] == "allow-all"
    ):
        yield viewer_p[2]

    if cache_beh := get_optional_attribute(
        graph, config_attrs, "CacheBehaviors"
    ):
        cb_attrs = graph.nodes[cache_beh[2]]["value_id"]
        for c_id in adj_ast(graph, cb_attrs):
            if (
                viewer_p := get_optional_attribute(
                    graph, c_id, "ViewerProtocolPolicy"
                )
            ) and viewer_p[1] == "allow-all":
                yield viewer_p[2]


def _serves_content_over_http(graph: Graph, nid: NId) -> Iterator[NId]:
    props = get_optional_attribute(graph, nid, "Properties")
    if not props:
        return
    val_id = graph.nodes[props[2]]["value_id"]
    if d_config := get_optional_attribute(graph, val_id, "DistributionConfig"):
        yield from _aux_serves_content_over_http(graph, d_config[2])


def cfn_serves_content_over_http(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_CONTENT_HTTP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::CloudFront::Distribution":
                for report in _serves_content_over_http(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f372.serves_content_over_http",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _elb2_uses_http_protocol(graph: Graph, nid: NId) -> NId | None:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return None
    val_id = graph.nodes[properties[2]]["value_id"]
    protocol = get_optional_attribute(graph, val_id, "Protocol")
    target = get_optional_attribute(graph, val_id, "TargetType")
    if (
        protocol
        and protocol[1] == "HTTP"
        and (not target or target[1] != "lambda")
    ):
        return protocol[2]
    return None


def cfn_elb2_uses_insecure_http_protocol(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::ElasticLoadBalancingV2::TargetGroup"
                and (report := _elb2_uses_http_protocol(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.elb2_uses_insecure_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
