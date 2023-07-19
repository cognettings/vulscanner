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


def _rds_has_unencrypted_storage(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    storage, storage_val, storage_id = get_attribute(
        graph, val_id, "StorageEncrypted"
    )
    if storage:
        if storage_val in FALSE_OPTIONS:
            yield storage_id
    else:
        yield prop_id


def cfn_rds_has_unencrypted_storage(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_UNENCRYPTED_STORAGE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in {
                "AWS::RDS::DBCluster",
                "AWS::RDS::DBInstance",
            }:
                for report in _rds_has_unencrypted_storage(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f246.rds_has_unencrypted_storage",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
