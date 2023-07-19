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


def _has_not_point_in_time_recovery(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    recovery, _, recovery_id = get_attribute(
        graph, val_id, "PointInTimeRecoverySpecification"
    )
    if not recovery:
        yield prop_id
    else:
        recovery_attrs = graph.nodes[recovery_id]["value_id"]
        point_rec, point_rec_val, point_rec_id = get_attribute(
            graph, recovery_attrs, "PointInTimeRecoveryEnabled"
        )
        if point_rec and point_rec_val in FALSE_OPTIONS:
            yield point_rec_id


def _dynamo_has_not_deletion_protection(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    deletion_prot, del_val, del_id = get_attribute(
        graph, val_id, "DeletionProtectionEnabled"
    )
    if not deletion_prot:
        yield prop_id
    elif del_val in FALSE_OPTIONS:
        yield del_id


def cfn_dynamo_has_not_deletion_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_DYNAMO_NOT_DEL_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::DynamoDB::Table":
                for report in _dynamo_has_not_deletion_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f259.dynamo_has_not_deletion_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_has_not_point_in_time_recovery(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_NOT_POINT_TIME_RECOVERY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::DynamoDB::Table":
                for report in _has_not_point_in_time_recovery(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("src.lib_path.f259.has_not_point_in_time_recovery"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
