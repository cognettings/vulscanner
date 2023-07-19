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


def _no_deletion_protection(graph: Graph, nid: NId) -> NId | None:
    attr = get_optional_attribute(graph, nid, "deletion_protection")
    if not attr:
        return nid
    if attr[1].lower() == "false":
        return attr[2]
    return None


def tfm_rds_no_deletion_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_NO_DELETION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_db_instance",
                "aws_rds_cluster",
            } and (report := _no_deletion_protection(graph, nid)):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f256.rds_has_not_termination_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_rds_has_not_automated_backups(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_NOT_AUTO_BACKUPS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name")
                in {"aws_rds_cluster", "aws_db_instance"}
                and (
                    report := get_optional_attribute(
                        graph, nid, "backup_retention_period"
                    )
                )
                and report[1] == "0"
            ):
                yield shard, report[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f256.rds_has_not_automated_backups",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
