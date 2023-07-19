from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
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


def _ec2_has_terminate_shutdown_behavior(graph: Graph, nid: NId) -> NId | None:
    shutdown = get_optional_attribute(
        graph, nid, "instance_initiated_shutdown_behavior"
    )
    if not shutdown:
        return nid
    if shutdown[1].lower() != "terminate":
        return shutdown[2]
    return None


def _aux_ec2_associate_public_ip_address(graph: Graph, nid: NId) -> NId | None:
    ip_address = get_optional_attribute(
        graph, nid, "associate_public_ip_address"
    )
    if ip_address and ip_address[1].lower() == "true":
        return ip_address[2]
    return None


def _ec2_associate_public_ip_address(graph: Graph, nid: NId) -> NId | None:
    obj_type = graph.nodes[nid].get("name")
    if obj_type and obj_type == "aws_instance":
        return _aux_ec2_associate_public_ip_address(graph, nid)
    expected_block = "network_interfaces"
    for c_id in adj_ast(graph, nid, name=expected_block):
        return _aux_ec2_associate_public_ip_address(graph, c_id)
    return None


def tfm_ec2_associate_public_ip_address(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_ASSOC_PUB_IP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_instance",
                "aws_launch_template",
            } and (report := _ec2_associate_public_ip_address(graph, nid)):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f333.ec2_public_ip_addresses",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_terminate_shutdown_behavior(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.EC2_TERMINATE_SHUTDOWN_BEHAVIOR

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_launch_template" and (
                report := _ec2_has_terminate_shutdown_behavior(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f333.tfm_ec2_allows_shutdown_command",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_not_an_iam_instance_profile(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_NO_IAM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get(
                "name"
            ) == "aws_instance" and not get_optional_attribute(
                graph, nid, "iam_instance_profile"
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f333.ec2_has_not_an_iam_instance_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
