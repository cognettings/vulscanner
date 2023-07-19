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


def _ebs_is_unencrypted(graph: Graph, nid: NId) -> NId | None:
    if not (attr := get_optional_attribute(graph, nid, "encrypted")):
        return nid
    if attr[1].lower() == "false":
        return attr[2]
    return None


def _ec2_unencrypted_ebs_block(graph: Graph, nid: NId) -> Iterator[NId]:
    for c_id in adj_ast(graph, nid, label_type="Object"):
        if graph.nodes[c_id]["name"] in {
            "root_block_device",
            "ebs_block_device",
        } and (report_id := _ebs_is_unencrypted(graph, c_id)):
            yield report_id


def tfm_ec2_unencrypted_ebs_block(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_UNENCRYPTED_BLOCK_DEVICES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_instance":
                for danger_id in _ec2_unencrypted_ebs_block(graph, nid):
                    yield shard, danger_id

    return get_vulnerabilities_from_n_ids(
        desc_key=("f250.tfm_ec2_instance_unencrypted_ebs_block_devices"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ebs_unencrypted_volumes(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EBS_UNENCRYPTED_VOLUMES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_ebs_volume" and (
                report := _ebs_is_unencrypted(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f250.resource_not_encrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ebs_unencrypted_by_default(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EBS_UNENCRYPTED_DEFAULT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name") == "aws_ebs_encryption_by_default"
                and (attr := get_optional_attribute(graph, nid, "enabled"))
                and attr[1].lower() == "false"
            ):
                yield shard, attr[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f250.tfm_ebs_unencrypted_by_default",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
