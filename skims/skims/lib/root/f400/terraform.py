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


def _ec2_monitoring_disabled(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "monitoring")
    if not attr:
        return nid
    if attr_val.lower() in {"false", "0"}:
        return attr_id
    return None


def _distribution_has_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    block = get_argument(graph, nid, "logging_config")
    if not block:
        return nid
    return None


def _trails_not_multiregion(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "is_multi_region_trail"
    )
    if not attr:
        return nid
    if attr_val.lower() not in {"true", "1"}:
        return attr_id
    return None


def _lb_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    access = get_argument(graph, nid, "access_logs")
    if not access:
        return nid
    attr, attr_val, attr_id = get_attribute(graph, access, "enabled")
    if attr and attr_val.lower() == "false":
        return attr_id
    return None


def tfm_load_balancers_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB_LOGGING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {"aws_elb", "aws_lb"} and (
                report := _lb_logging_disabled(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_trails_not_multiregion(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_TRAILS_NOT_MULTIREGION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_cloudtrail":
                if report := _trails_not_multiregion(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.trails_not_multiregion",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_distribution_has_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_CF_DISTR_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_cloudfront_distribution":
                if report := _distribution_has_logging_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.tfm_has_logging_config_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_monitoring_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_MONITORING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_instance":
                if report := _ec2_monitoring_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f400.has_monitoring_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
