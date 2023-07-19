from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
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


def _rds_has_not_termination_protection(graph: Graph, nid: NId) -> NId | None:
    props = get_optional_attribute(graph, nid, "Properties")
    if not props:
        return None
    val_id = graph.nodes[props[2]]["value_id"]
    deletion_prot = get_optional_attribute(graph, val_id, "DeletionProtection")
    if not deletion_prot:
        return props[2]
    if deletion_prot[1] in FALSE_OPTIONS:
        return deletion_prot[2]
    return None


def _rds_has_not_automated_backups(graph: Graph, nid: NId) -> NId | None:
    props = get_optional_attribute(graph, nid, "Properties")
    if not props:
        return None
    val_id = graph.nodes[props[2]]["value_id"]
    backup = get_optional_attribute(graph, val_id, "BackupRetentionPeriod")
    if backup and backup[1] in (0, "0"):
        return backup[2]
    return None


def cfn_rds_has_not_automated_backups(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_NOT_AUTO_BACKUPS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1]
                in {
                    "AWS::RDS::DBCluster",
                    "AWS::RDS::DBInstance",
                }
                and (report := _rds_has_not_automated_backups(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f256.rds_has_not_automated_backups",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_rds_has_not_termination_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_NOT_TERMINATION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1]
                in {
                    "AWS::RDS::DBCluster",
                    "AWS::RDS::DBInstance",
                }
                and (report := _rds_has_not_termination_protection(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f256.rds_has_not_termination_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
