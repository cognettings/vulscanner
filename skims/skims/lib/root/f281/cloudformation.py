from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
    TRUE_OPTIONS,
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


def _bucket_policy_has_secure_transport(
    graph: Graph, nid: NId
) -> Iterator[NId]:
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
            if not (effect := get_optional_attribute(graph, stmt, "Effect")):
                continue
            sec_trans = get_optional_attribute_inside_path(
                graph, stmt, ["Condition", "Bool", "aws:SecureTransport"]
            )
            if sec_trans and (
                (effect[1] == "Deny" and sec_trans[1] in TRUE_OPTIONS)
                or (effect[1] == "Allow" and sec_trans[1] in FALSE_OPTIONS)
            ):
                yield sec_trans[2]


def cfn_bucket_policy_has_secure_transport(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_BUCKET_POLICY_SEC_TRANSPORT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::S3::BucketPolicy":
                for report in _bucket_policy_has_secure_transport(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f281.bucket_policy_has_secure_transport",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
