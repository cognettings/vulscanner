from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
)
from lib.root.utilities.cloudformation import (
    get_attribute,
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


def _bucket_has_logging_conf_disabled(graph: Graph, nid: NId) -> NId | None:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if not get_optional_attribute(graph, val_id, "LoggingConfiguration"):
        return prop_id
    return None


def _cf_dist_has_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if d_config := get_optional_attribute(graph, val_id, "DistributionConfig"):
        data_id = graph.nodes[d_config[2]]["value_id"]
        logging, _, _ = get_attribute(graph, data_id, "Logging")
        if not logging:
            return d_config[2]
    return None


def _elb2_has_access_logs_s3_disabled(graph: Graph, nid: NId) -> NId | None:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]

    if not (
        load_bal := get_optional_attribute(
            graph, val_id, "LoadBalancerAttributes"
        )
    ):
        return prop_id
    key_exist = False
    load_attrs = graph.nodes[load_bal[2]]["value_id"]
    for c_id in adj_ast(graph, load_attrs):
        if (key := get_optional_attribute(graph, c_id, "Key")) and key[
            1
        ] == "access_logs.s3.enabled":
            key_exist = True
            value = get_optional_attribute(graph, c_id, "Value")
            if value and value[1] in FALSE_OPTIONS:
                return value[2]
    if not key_exist:
        return load_bal[2]
    return None


def _elb_has_access_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    access_log = get_optional_attribute(graph, val_id, "AccessLoggingPolicy")
    if not access_log:
        return prop_id
    val_id = graph.nodes[access_log[2]]["value_id"]
    enabled = get_optional_attribute(graph, val_id, "Enabled")
    if not enabled:
        return access_log[2]
    if enabled[1] in FALSE_OPTIONS:
        return enabled[2]
    return None


def _ec2_monitoring_disabled(graph: Graph, nid: NId) -> NId | None:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    monitoring = get_optional_attribute(graph, val_id, "Monitoring")
    if not monitoring:
        return prop_id
    if monitoring[1] in FALSE_OPTIONS:
        return monitoring[2]
    return None


def _trails_not_multiregion(graph: Graph, nid: NId) -> NId | None:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    trail = get_optional_attribute(graph, val_id, "IsMultiRegionTrail")
    if not trail:
        return prop_id
    if trail[1] in FALSE_OPTIONS:
        return trail[2]
    return None


def cfn_trails_not_multiregion(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_TRAILS_NOT_MULTIREGION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::CloudTrail::Trail"
                and (report := _trails_not_multiregion(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.trails_not_multiregion",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_monitoring_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_MONITORING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::EC2::Instance"
                and (report := _ec2_monitoring_disabled(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.has_monitoring_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_elb_has_access_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB_ACCESS_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::ElasticLoadBalancing::LoadBalancer"
                and (report := _elb_has_access_logging_disabled(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.elb_has_access_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_elb2_has_access_logs_s3_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_LOGS_S3_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::ElasticLoadBalancingV2::LoadBalancer"
                and (report := _elb2_has_access_logs_s3_disabled(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.elb2_has_access_logs_s3_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_cf_distribution_has_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_CF_DISTR_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::CloudFront::Distribution"
                and (report := _cf_dist_has_logging_disabled(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_bucket_has_logging_conf_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_LOG_CONF_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::S3::Bucket"
                and (report := _bucket_has_logging_conf_disabled(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.bucket_has_logging_conf_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
