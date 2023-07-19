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
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def tfm_rds_publicly_accessible(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_PUB_ACCESSIBLE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name")
                in {
                    "aws_rds_cluster_instance",
                    "aws_db_instance",
                }
                and (
                    pub_access := get_optional_attribute(
                        graph, nid, "publicly_accessible"
                    )
                )
                and pub_access[1] == "true"
            ):
                yield shard, pub_access[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f073.rds_is_publicly_accessible",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
