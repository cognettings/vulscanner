from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
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


def _aws_efs_unencrypted(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(graph, nid, "encrypted")
    if not attr:
        return nid
    if attr_val.lower() == "false":
        return attr_id
    return None


def tfm_aws_efs_unencrypted(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EFS_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_efs_file_system" and (
                report := _aws_efs_unencrypted(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f406.aws_efs_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
