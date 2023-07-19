from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
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


def _ec2_unencrypted_ebs_block(graph: Graph, nid: NId) -> Iterator[NId]:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return
    val_id = graph.nodes[properties[2]]["value_id"]
    if mapps := get_optional_attribute(graph, val_id, "BlockDeviceMappings"):
        mappings_attr = graph.nodes[mapps[2]]["value_id"]
        for c_id in adj_ast(graph, mappings_attr):
            if ebs := get_optional_attribute(graph, c_id, "Ebs"):
                ebs_attrs = graph.nodes[ebs[2]]["value_id"]
                encryp = get_optional_attribute(graph, ebs_attrs, "Encrypted")
                if not encryp:
                    yield ebs[2]
                elif encryp[1] in FALSE_OPTIONS:
                    yield encryp[2]


def _ec2_has_unencrypted_volumes(graph: Graph, nid: NId) -> NId | None:
    danger_id = None
    if (props := get_optional_attribute(graph, nid, "Properties")) and (
        val_id := graph.nodes[props[2]]["value_id"]
    ):
        encrypted = get_optional_attribute(graph, val_id, "Encrypted")
        if not encrypted:
            danger_id = props[2]
        else:
            if encrypted[1] in FALSE_OPTIONS:
                danger_id = encrypted[2]
            elif not get_optional_attribute(graph, val_id, "KmsKeyId"):
                danger_id = props[2]
    return danger_id


def cfn_ec2_has_unencrypted_volumes(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNENCRYPTED_VOLUMES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::EC2::Volume"
                and (report := _ec2_has_unencrypted_volumes(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f250.ec2_has_unencrypted_volumes"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_unencrypted_ebs_block(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNENCRYPTED_BLOCK_DEVICES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::EC2::Instance":
                for report in _ec2_unencrypted_ebs_block(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f250.cfn_ec2_instance_unencrypted_ebs_block_devices"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
