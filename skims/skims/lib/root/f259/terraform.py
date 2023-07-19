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


def _db_no_point_in_time_recovery(graph: Graph, nid: NId) -> NId | None:
    if point := get_argument(graph, nid, "point_in_time_recovery"):
        attr, attr_val, attr_id = get_attribute(graph, point, "enabled")
        if not attr:
            return nid
        if attr_val.lower() == "false":
            return attr_id
    return None


def _dynamo_has_not_deletion_protection(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "deletion_protection_enabled"
    )
    if not attr:
        yield nid
    if attr_val.lower() == "false":
        yield attr_id


def tfm_dynamo_has_not_deletion_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DYNAMO_NOT_DEL_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_dynamodb_table":
                for report in _dynamo_has_not_deletion_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f259.dynamo_has_not_deletion_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_db_no_point_in_time_recovery(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_DB_NO_POINT_TIME_RECOVERY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_dynamodb_table" and (
                report := _db_no_point_in_time_recovery(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f259.has_not_point_in_time_recovery",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
