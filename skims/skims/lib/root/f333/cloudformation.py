from collections.abc import (
    Iterator,
)
from lib.path.common import (
    TRUE_OPTIONS,
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


def _ec2_has_not_an_iam_instance_profile(graph: Graph, nid: NId) -> NId | None:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return None
    val_id = graph.nodes[properties[2]]["value_id"]

    launch_data = get_optional_attribute(graph, val_id, "LaunchTemplateData")
    data_id = val_id
    report_id = properties[2]
    if launch_data:
        data_id = graph.nodes[launch_data[2]]["value_id"]
        report_id = launch_data[2]
    if not get_optional_attribute(graph, data_id, "IamInstanceProfile"):
        return report_id
    return None


def _ec2_has_terminate_shutdown_behavior(graph: Graph, nid: NId) -> NId | None:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return None
    val_id = graph.nodes[properties[2]]["value_id"]
    launch_data = get_optional_attribute(graph, val_id, "LaunchTemplateData")
    if launch_data:
        data_id = graph.nodes[launch_data[2]]["value_id"]
        terminate = get_optional_attribute(
            graph, data_id, "InstanceInitiatedShutdownBehavior"
        )
        if not terminate:
            return launch_data[2]
        if terminate[1] != "terminate":
            return terminate[2]
    else:
        return properties[2]
    return None


def _ec2_associate_public_ip_address(graph: Graph, nid: NId) -> Iterator[NId]:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return
    val_id = graph.nodes[properties[2]]["value_id"]
    launch_data = get_optional_attribute(graph, val_id, "LaunchTemplateData")
    data_id = val_id
    if launch_data:
        data_id = graph.nodes[launch_data[2]]["value_id"]
    net_interface = get_optional_attribute(graph, data_id, "NetworkInterfaces")
    if net_interface:
        ni_attrs = graph.nodes[net_interface[2]]["value_id"]
        for c_id in adj_ast(graph, ni_attrs):
            public_ip = get_optional_attribute(
                graph, c_id, "AssociatePublicIpAddress"
            )
            if public_ip and public_ip[1] in TRUE_OPTIONS:
                yield public_ip[2]


def cfn_ec2_associate_public_ip_address(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_ASSOC_PUB_IP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in {
                "AWS::EC2::LaunchTemplate",
                "AWS::EC2::Instance",
            }:
                for report in _ec2_associate_public_ip_address(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f333.cfn_ec2_associate_public_ip_address",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_terminate_shutdown_behavior(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_TERMINATE_SHUTDOWN_BEHAVIOR

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::EC2::LaunchTemplate"
                and (
                    report := _ec2_has_terminate_shutdown_behavior(graph, nid)
                )
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f333.cfn_ec2_allows_shutdown_command",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_not_an_iam_instance_profile(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_NO_IAM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::EC2::Instance"
                and (
                    report := _ec2_has_not_an_iam_instance_profile(graph, nid)
                )
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f333.ec2_has_not_an_iam_instance_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
