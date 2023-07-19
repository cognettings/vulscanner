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


def _aws_ebs_volumes_unencrypted(graph: Graph, nid: NId) -> NId | None:
    if root := get_argument(graph, nid, "root_block_device"):
        attr, attr_val, attr_id = get_attribute(graph, root, "encrypted")
        if not attr:
            return root
        if attr_val.lower() == "false":
            return attr_id
    else:
        return nid
    return None


def tfm_aws_ebs_volumes_unencrypted(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EBS_VOLUMES_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_launch_configuration" and (
                report := _aws_ebs_volumes_unencrypted(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f407.tfm_aws_ebs_volumes_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
