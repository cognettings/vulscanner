from collections.abc import (
    Iterator,
)
from lib.root.f016.terraform import (
    VULNERABLE_MIN_PROT_VERSIONS,
    VULNERABLE_ORIGIN_SSL_PROTOCOLS as VULN_ORIGIN_SSL_PROTOCOLS,
)
from lib.root.utilities.cloudformation import (
    get_key_value,
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
    match_ast_d,
    match_ast_group_d,
)


def _elb_without_sslpolicy(graph: Graph, nid: NId) -> NId | None:
    if not (prop := get_optional_attribute(graph, nid, "Properties")):
        return None
    val_id = graph.nodes[prop[2]]["value_id"]

    if ssl_pol := get_optional_attribute(graph, val_id, "SslPolicy"):
        ssl_pol_val = ssl_pol[1]
        if ssl_pol_val in {
            "ELBSecurityPolicy-2016-08",
            "ELBSecurityPolicy-TLS-1-0-2015-04",
        }:
            return ssl_pol[2]
        return None

    if def_act := get_optional_attribute(graph, val_id, "DefaultActions"):
        for pair in match_ast_group_d(graph, def_act[2], "Pair", depth=-1):
            if get_key_value(graph, pair) == ("Type", "redirect"):
                return None
    return prop[2]


def _helper_insecure_protocols(graph: Graph, nid: NId) -> Iterator[NId]:
    if (
        (object_id := match_ast_d(graph, nid, "Object"))
        and (
            c_origin := get_optional_attribute(
                graph, object_id, "CustomOriginConfig"
            )
        )
        and (custom_attrs := graph.nodes[c_origin[2]]["value_id"])
        and (
            ssl_prot := get_optional_attribute(
                graph, custom_attrs, "OriginSSLProtocols"
            )
        )
    ):
        ssl_list_id = graph.nodes[ssl_prot[2]]["value_id"]
        for c_id in adj_ast(graph, ssl_list_id):
            if graph.nodes[c_id].get("value") in VULN_ORIGIN_SSL_PROTOCOLS:
                yield c_id


def _serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if (
        (prop := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[prop[2]]["value_id"])
        and (
            dist_config := get_optional_attribute(
                graph, val_id, "DistributionConfig"
            )
        )
        and (dist_attrs := graph.nodes[dist_config[2]]["value_id"])
    ):
        if (
            (
                v_cert := get_optional_attribute(
                    graph, dist_attrs, "ViewerCertificate"
                )
            )
            and (v_attrs := graph.nodes[v_cert[2]]["value_id"])
            and (
                min_prot := get_optional_attribute(
                    graph, v_attrs, "MinimumProtocolVersion"
                )
            )
            and min_prot[1] in VULNERABLE_MIN_PROT_VERSIONS
        ):
            yield min_prot[2]
        if origins := get_optional_attribute(graph, dist_attrs, "Origins"):
            origin_attr = graph.nodes[origins[2]]["value_id"]
            yield from _helper_insecure_protocols(graph, origin_attr)


def cfn_serves_content_over_insecure_protocols(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in {"AWS::CloudFront::Distribution"}:
                for report in _serves_content_over_insecure_protocols(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_elb_without_sslpolicy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB_WITHOUT_SSLPOLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] in {"AWS::ElasticLoadBalancingV2::Listener"}
                and (report := _elb_without_sslpolicy(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.aws_elb_without_sslpolicy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
