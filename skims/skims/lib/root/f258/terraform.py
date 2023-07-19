from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
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


def _elb2_has_not_deletion_protection(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "enable_deletion_protection"
    )
    if not attr:
        return nid
    if attr_val.lower() in {"false", "0"}:
        return attr_id
    return None


def tfm_elb2_has_not_deletion_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_NOT_DELETION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_lb" and (
                report := _elb2_has_not_deletion_protection(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f258.elb2_has_not_deletion_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
