from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_list_from_node,
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
from utils.graph import (
    match_ast_group_d,
)


def _cors_uses_danger_methods(graph: Graph, nid: NId) -> Iterator[NId]:
    for c_id in match_ast_group_d(graph, nid, "Object"):
        if (
            graph.nodes[c_id].get("name") == "cors_rule"
            and (
                allow_origins := get_optional_attribute(
                    graph, c_id, "allowed_origins"
                )
            )
            and (methods := get_list_from_node(graph, allow_origins[2]))
            and "*" in methods
        ):
            yield allow_origins[2]


def tfm_wildcard_in_allowed_origins(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_WILDCARD_IN_ALLOWED_ORIGINS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name")
                == "aws_s3_bucket_cors_configuration"
            ):
                for report in _cors_uses_danger_methods(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.wildcard_in_allowed_origins",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
