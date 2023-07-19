from collections.abc import (
    Iterator,
)
from lib.path.common import (
    TRUE_OPTIONS,
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


def _rds_is_publicly_accessible(graph: Graph, nid: NId) -> NId | None:
    if (
        (props := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[props[2]]["value_id"])
        and (
            public := get_optional_attribute(
                graph, val_id, "PubliclyAccessible"
            )
        )
        and public[1] in TRUE_OPTIONS
    ):
        return public[2]
    return None


def cfn_rds_is_publicly_accessible(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_RDS_PUB_ACCESSIBLE

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
                and (report := _rds_is_publicly_accessible(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f073.rds_is_publicly_accessible",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
