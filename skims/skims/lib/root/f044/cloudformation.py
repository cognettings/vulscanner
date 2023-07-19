from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
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
    adj_ast,
)


def _all_http_methods_enabled(graph: Graph, val_id: NId) -> NId | None:
    if (
        m_settings := get_optional_attribute(graph, val_id, "MethodSettings")
    ) and (m_attrs := graph.nodes[m_settings[2]]["value_id"]):
        for c_id in adj_ast(graph, m_attrs):
            if (
                http_m := get_optional_attribute(graph, c_id, "HttpMethod")
            ) and http_m[1] == "*":
                return http_m[2]
    return None


def cfn_api_all_http_methods_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_HTTP_METHODS_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::Serverless::Api"
                and (
                    properties := get_optional_attribute(
                        graph, nid, "Properties"
                    )
                )
                and (val_id := graph.nodes[properties[2]]["value_id"])
                and (report := _all_http_methods_enabled(graph, val_id))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f044.resource_has_https_methods_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _danger_https_methods_enabled(graph: Graph, val_id: NId) -> Iterator[NId]:
    if (
        (config := get_optional_attribute(graph, val_id, "CorsConfiguration"))
        and (config_attrs := graph.nodes[config[2]]["value_id"])
        and (rules := get_optional_attribute(graph, config_attrs, "CorsRules"))
        and (rules_obj := graph.nodes[rules[2]]["value_id"])
    ):
        for c_id in adj_ast(graph, rules_obj):
            if (
                (
                    allowed_m := get_optional_attribute(
                        graph, c_id, "AllowedMethods"
                    )
                )
                and (methods := get_list_from_node(graph, allowed_m[2]))
                and ("POST" in methods or "DELETE" in methods)
            ):
                yield allowed_m[2]


def cfn_has_danger_https_methods_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_HTTP_METHODS_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::S3::Bucket"
                and (
                    properties := get_optional_attribute(
                        graph, nid, "Properties"
                    )
                )
                and (val_id := graph.nodes[properties[2]]["value_id"])
            ):
                for report in _danger_https_methods_enabled(graph, val_id):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f044.resource_has_danger_https_methods_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
