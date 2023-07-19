from collections.abc import (
    Iterator,
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


def _s3_bucket_versioning_disabled(graph: Graph, nid: NId) -> NId | None:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return None
    val_id = graph.nodes[properties[2]]["value_id"]
    version = get_optional_attribute(graph, val_id, "VersioningConfiguration")
    if version:
        data_id = graph.nodes[version[2]]["value_id"]
        status = get_optional_attribute(graph, data_id, "Status")
        if not status:
            return version[2]
        if status[1] != "Enabled":
            return status[2]
    else:
        return properties[2]
    return None


def cfn_s3_bucket_versioning_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_S3_VERSIONING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::S3::Bucket"
                and (report := _s3_bucket_versioning_disabled(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f335.cfn_s3_bucket_versioning_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
