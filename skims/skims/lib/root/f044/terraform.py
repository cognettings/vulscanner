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


def tfm_api_all_http_methods_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_API_ALL_HTTP_METHODS_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name") == "aws_api_gateway_method"
                and (
                    http_m := get_optional_attribute(graph, nid, "http_method")
                )
                and http_m[1] == "ANY"
            ):
                yield shard, http_m[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f044.resource_has_https_methods_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _cors_uses_danger_methods(graph: Graph, nid: NId) -> Iterator[NId]:
    for c_id in match_ast_group_d(graph, nid, "Object"):
        if (
            graph.nodes[c_id].get("name") == "cors_rule"
            and (
                allow_methods := get_optional_attribute(
                    graph, c_id, "allowed_methods"
                )
            )
            and (methods := get_list_from_node(graph, allow_methods[2]))
            and ("POST" in methods or "DELETE" in methods)
        ):
            yield allow_methods[2]


def tfm_has_danger_https_methods_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_HTTP_METHODS_ENABLED

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
        desc_key="f044.resource_has_danger_https_methods_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
