from collections.abc import (
    Iterator,
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


def _public_buckets(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    access, access_val, access_id = get_attribute(
        graph, val_id, "AccessControl"
    )
    if access and access_val == "PublicReadWrite":
        yield access_id


def cfn_public_buckets(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_PUBLIC_BUCKETS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::S3::Bucket":
                for report in _public_buckets(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f203.public_buckets",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
