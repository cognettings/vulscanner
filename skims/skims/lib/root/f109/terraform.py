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


def tfm_rds_not_inside_subnet(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_RDS_INSIDE_SUBNET

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_rds_cluster",
                "aws_db_instance",
            } and not get_optional_attribute(
                graph, nid, "db_subnet_group_name"
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f109.rds_is_not_inside_a_db_subnet_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
