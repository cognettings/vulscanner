from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
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


def cfn_rds_is_not_inside_a_db_subnet_group(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_NOT_INSIDE_DB_SUBNET

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
                and (props := get_optional_attribute(graph, nid, "Properties"))
                and (val_id := graph.nodes[props[2]]["value_id"])
                and not get_optional_attribute(
                    graph, val_id, "DBSubnetGroupName"
                )
            ):
                yield shard, props[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f109.rds_is_not_inside_a_db_subnet_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
