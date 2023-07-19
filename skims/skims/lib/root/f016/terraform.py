from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_attribute,
    get_optional_attribute,
    list_has_string,
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

VULNERABLE_ORIGIN_SSL_PROTOCOLS = ["SSLv3", "TLSv1", "TLSv1.1"]
VULNERABLE_MIN_PROT_VERSIONS = [
    "SSLv3",
    "TLSv1",
    "TLSv1_2016",
    "TLSv1.1_2016",
]


def _azure_serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> NId | None:
    attr, attr_value, attr_id = get_attribute(graph, nid, "min_tls_version")
    if not attr:
        return nid
    if attr_value in ("TLS1_0", "TLS1_1"):
        return attr_id
    return None


def _aws_elb_without_sslpolicy(graph: Graph, nid: NId) -> NId | None:
    expected_attr = get_attribute(graph, nid, "ssl_policy")
    if not expected_attr[0]:
        return nid
    return None


def has_vuln_ssl(graph: Graph, nid: NId) -> bool:
    array_id = graph.nodes[nid]["value_id"]
    for prot in VULNERABLE_ORIGIN_SSL_PROTOCOLS:
        if list_has_string(graph, array_id, prot):
            return True
    return False


def _aws_serves_content_over_insecure_protocols(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if (
        (v_cert := get_argument(graph, nid, "viewer_certificate"))
        and (
            min_prot := get_attribute(
                graph, v_cert, "minimum_protocol_version"
            )
        )
        and any(
            True
            for protocol in VULNERABLE_MIN_PROT_VERSIONS
            if protocol == min_prot[1]
        )
    ):
        yield min_prot[2]
    if (
        (origin := get_argument(graph, nid, "origin"))
        and (argument := get_argument(graph, origin, "custom_origin_config"))
        and (
            ssl_prot := get_optional_attribute(
                graph, argument, "origin_ssl_protocols"
            )
        )
        and has_vuln_ssl(graph, ssl_prot[2])
    ):
        yield ssl_prot[2]


def _az_api_insecure_protocols(graph: Graph, nid: NId) -> NId | None:
    if (
        (properties := get_optional_attribute(graph, nid, "properties"))
        and (
            site_config := get_optional_attribute(
                graph, graph.nodes[properties[2]]["value_id"], "siteConfig"
            )
        )
        and (
            tls_version := get_optional_attribute(
                graph, graph.nodes[site_config[2]]["value_id"], "minTlsVersion"
            )
        )
        and tls_version[1] in {"1.0", "1.1"}
    ):
        return tls_version[2]
    return None


def tfm_aws_serves_content_over_insecure_protocols(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                name := graph.nodes[node].get("name")
            ) and name == "aws_cloudfront_distribution":
                for nid in _aws_serves_content_over_insecure_protocols(
                    graph, node
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_serves_content_over_insecure_protocols(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                (name := graph.nodes[node].get("name"))
                and name == "azurerm_storage_account"
                and (
                    report := _azure_serves_content_over_insecure_protocols(
                        graph, node
                    )
                )
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_api_insecure_protocols(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_INSEC_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        """
        Sources:
        https://docs.fugue.co/FG_R00347.html
        https://docs.bridgecrew.io/docs/bc_azr_networking_6
        """
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                (name := graph.nodes[node].get("name"))
                and name == "azapi_resource"
                and (tls_vuln := _az_api_insecure_protocols(graph, node))
            ):
                yield shard, tls_vuln

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.serves_content_over_insecure_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_elb_without_sslpolicy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_ELB_WITHOUT_SSLPOLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                (name := graph.nodes[node].get("name"))
                and name == "aws_lb_listener"
                and (report := _aws_elb_without_sslpolicy(graph, node))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f016.aws_elb_without_sslpolicy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
