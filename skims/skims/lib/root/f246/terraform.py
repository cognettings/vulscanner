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


def _has_unencrypted_storage(graph: Graph, nid: NId) -> NId | None:
    attr = get_optional_attribute(graph, nid, "storage_encrypted")
    if not attr:
        return nid
    if attr[1].lower() == "false":
        return attr[2]
    return None


def tfm_rds_has_unencrypted_storage(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_UNENCRYPTED_STORAGE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_db_instance",
                "aws_rds_cluster",
            } and (report := _has_unencrypted_storage(graph, nid)):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f246.rds_has_unencrypted_storage",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
