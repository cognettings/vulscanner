from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
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
from utils.graph import (
    adj_ast,
)


def _secgroup_uses_insecure_protocol(graph: Graph, nid: NId) -> Iterator[NId]:
    properties = get_optional_attribute(graph, nid, "Properties")
    if not properties:
        return
    val_id = graph.nodes[properties[2]]["value_id"]
    if ingress := get_optional_attribute(
        graph, val_id, "SecurityGroupIngress"
    ):
        traffic_attrs = graph.nodes[ingress[2]]["value_id"]
        for c_id in adj_ast(graph, traffic_attrs):
            if (
                (protocol := get_optional_attribute(graph, c_id, "IpProtocol"))
                and protocol[1] in ("tcp", "-1")
                and (
                    init_port := get_optional_attribute(
                        graph, c_id, "FromPort"
                    )
                )
                and init_port[1] == "80"
            ):
                yield protocol[2]


def cfn_secgroup_uses_insecure_protocol(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_AWS_SEC_GROUP_USING_TCP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::EC2::SecurityGroup":
                for report in _secgroup_uses_insecure_protocol(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.tfm_aws_sec_group_using_tcp",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _server_ssl_disabled(graph: Graph, n_id: NId) -> NId | None:
    val_id = graph.nodes[n_id]["value_id"]
    ssl_config = get_optional_attribute(graph, val_id, "ssl")
    if (
        ssl_config
        and (config_id := graph.nodes[ssl_config[2]]["value_id"])
        and (
            ssl_enabled := get_optional_attribute(graph, config_id, "enabled")
        )
        and ssl_enabled[1] in FALSE_OPTIONS
    ):
        return ssl_enabled[2]
    return None


def cfn_server_disabled_ssl(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_SERVER_SSL_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key_id = graph.nodes[nid]["key_id"]
            if graph.nodes[key_id]["value"] == "server" and (
                vuln_id := _server_ssl_disabled(graph, nid)
            ):
                yield shard, vuln_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.container_disabled_ssl",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
