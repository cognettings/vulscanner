from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
    get_optional_attribute,
)
from lib.root.utilities.kubernetes import (
    check_template_integrity,
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


def _insecure_port(graph: Graph, nid: NId) -> Iterator[NId]:
    if ports := get_optional_attribute(graph, nid, "ports"):
        ports_attrs = graph.nodes[ports[2]]["value_id"]
        for port_id in adj_ast(graph, ports_attrs):
            if (
                (port := get_optional_attribute(graph, port_id, "port"))
                and (
                    protocol := get_optional_attribute(
                        graph, port_id, "protocol"
                    )
                )
                and port[1] == "80"
                and protocol[1] == "TCP"
            ):
                yield port_id


def k8s_insecure_port(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KUBERNETES_INSECURE_PORT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                check_template_integrity(graph, nid)
                and (spec_id := get_optional_attribute(graph, nid, "spec"))
                and (t_id := graph.nodes[spec_id[2]]["value_id"])
            ):
                for report in _insecure_port(graph, t_id):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.use_insecure_http_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def k8s_insecure_http_channel(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KUBERNETES_USES_HTTP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key_id = graph.nodes[nid]["key_id"]
            value_id = graph.nodes[nid]["value_id"]
            if (
                graph.nodes[key_id]["value"]
                in {"livenessProbe", "startupProbe", "readinessProbe"}
                and (
                    http_get := get_optional_attribute(
                        graph, value_id, "httpGet"
                    )
                )
                and (specs_attrs := graph.nodes[http_get[2]]["value_id"])
                and (
                    scheme := get_optional_attribute(
                        graph, specs_attrs, "scheme"
                    )
                )
                and scheme[1] in {"http", "HTTP"}
            ):
                yield shard, scheme[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.use_insecure_http_protocol",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
