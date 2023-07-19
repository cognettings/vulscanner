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


def _aws_efs_unencrypted(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    encrypted, encrypted_val, encrypted_id = get_attribute(
        graph, val_id, "Encrypted"
    )
    if not encrypted:
        yield prop_id
    elif encrypted_val in FALSE_OPTIONS:
        yield encrypted_id


def cfn_aws_efs_unencrypted(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_AWS_EFS_UNENCRYPTED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::EFS::FileSystem":
                for report in _aws_efs_unencrypted(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f406.aws_efs_unencrypted",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
