from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    get_attribute,
    is_parent,
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


def is_in_path(graph: Graph, nid: NId) -> Iterator[NId]:
    correct_parents = ["Statement"]
    effect, effect_val, _ = get_attribute(graph, nid, "Effect")
    principal, principa_val, principal_id = get_attribute(
        graph, nid, "Principal"
    )
    if (
        effect
        and principal
        and principa_val == "*"
        and effect_val == "Allow"
        and is_parent(graph, principal_id, correct_parents)
    ):
        yield principal_id


def json_principal_wildcard(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSON_PRINCIPAL_WILDCARD

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            for report in is_in_path(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f325.json_principal_wildcard",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
