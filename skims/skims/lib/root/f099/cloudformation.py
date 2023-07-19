from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
)
from lib.root.utilities.cloudformation import (
    get_optional_attribute,
    get_optional_attribute_inside_path,
    yield_statements_from_policy,
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


def _bucket_ss_enc_disabled(graph: Graph, nid: NId) -> Iterator[NId]:
    if (
        (props := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[props[2]]["value_id"])
        and (
            pol_doc := get_optional_attribute(graph, val_id, "PolicyDocument")
        )
    ):
        for stmt in yield_statements_from_policy(
            graph, graph.nodes[pol_doc[2]]["value_id"]
        ):
            if (
                (effect := get_optional_attribute(graph, stmt, "Effect"))
                and effect[1] == "Allow"
                and (
                    ss_enc := get_optional_attribute_inside_path(
                        graph,
                        stmt,
                        [
                            "Condition",
                            "Null",
                            "s3:x-amz-server-side-encryption",
                        ],
                    )
                )
                and ss_enc[1] in FALSE_OPTIONS
            ):
                yield ss_enc[2]


def cfn_bucket_server_side_encryption_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_POLICY_SERVER_ENCRYP_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::S3::BucketPolicy":
                for report in _bucket_ss_enc_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f099.s3_has_server_side_encryption_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
