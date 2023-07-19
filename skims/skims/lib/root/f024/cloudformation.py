from collections.abc import (
    Iterator,
)
from contextlib import (
    suppress,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from lib.root.utilities.cloudformation import (
    get_key_value,
    get_optional_attribute,
    is_cidr,
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
    matching_nodes,
    pred_ast,
)
from utils.graph.text_nodes import (
    node_to_values,
)

PUBLIC_CIDRS = {"::/0", "0.0.0.0/0"}


def _instances_without_profile(graph: Graph, nid: NId) -> NId | None:
    if (
        (prop := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[prop[2]]["value_id"])
        and not get_optional_attribute(graph, val_id, "IamInstanceProfile")
    ):
        return prop[2]

    return None


def _group_without_egress(graph: Graph, nid: NId) -> NId | None:
    prop = get_optional_attribute(graph, nid, "Properties")
    if not prop:
        return None

    val_id = graph.nodes[prop[2]]["value_id"]
    if get_optional_attribute(
        graph, val_id, "SecurityGroupEgress"
    ) or not get_optional_attribute(graph, val_id, "SecurityGroupIngress"):
        return None

    group_ref = None
    if (parent := pred_ast(graph, nid)[0]) and graph.nodes[parent][
        "label_type"
    ] == "Pair":
        group_ref = get_key_value(graph, parent)[0]

    if not group_ref:
        return prop[2]

    for obj_id in matching_nodes(graph, label_type="Object"):
        if (
            (resource := get_optional_attribute(graph, obj_id, "Type"))
            and resource[1] == "AWS::EC2::SecurityGroupEgress"
            and (prop_2 := get_optional_attribute(graph, obj_id, "Properties"))
        ):
            val_id = graph.nodes[prop_2[2]]["value_id"]
            if (
                group_id := get_optional_attribute(graph, val_id, "GroupId")
            ) and group_ref in node_to_values(graph, group_id[2]):
                return None
    return prop[2]


def _unrestricted_ip_protocols(graph: Graph, nid: NId) -> NId | None:
    ip_protocol = get_optional_attribute(graph, nid, "IpProtocol")
    if ip_protocol and ip_protocol[1] in (-1, "-1"):
        return ip_protocol[2]
    return None


def _ec2_has_unrestricted_ports(graph: Graph, nid: NId) -> NId | None:
    if (
        (from_port := get_optional_attribute(graph, nid, "FromPort"))
        and (to_port := get_optional_attribute(graph, nid, "ToPort"))
        and int(from_port[1]) != int(to_port[1])
        and abs(int(to_port[1]) - int(from_port[1])) > 25
    ):
        return from_port[2]
    return None


def _ec2_has_unrestricted_ftp_access(graph: Graph, nid: NId) -> Iterator[NId]:
    cidr = get_optional_attribute(
        graph, nid, "CidrIp"
    ) or get_optional_attribute(graph, nid, "CidrIpv6")

    if (
        cidr
        and cidr[1] in PUBLIC_CIDRS
        and (to_port := get_optional_attribute(graph, nid, "ToPort"))
        and (from_port := get_optional_attribute(graph, nid, "FromPort"))
    ):
        ip_prot = get_optional_attribute(graph, nid, "IpProtocol")
        if (
            ip_prot
            and ip_prot[1] in ("tcp", "-1")
            and any(
                float(from_port[1]) <= port <= float(to_port[1])
                for port in range(20, 22)
            )
        ):
            yield from_port[2]


def _ec2_has_unrestricted_dns_access(graph: Graph, nid: NId) -> NId | None:
    cidr = get_optional_attribute(
        graph, nid, "CidrIp"
    ) or get_optional_attribute(graph, nid, "CidrIpv6")

    if (
        cidr
        and cidr[1] in PUBLIC_CIDRS
        and (to_port := get_optional_attribute(graph, nid, "ToPort"))
        and (from_port := get_optional_attribute(graph, nid, "FromPort"))
        and float(from_port[1]) <= 53 <= float(to_port[1])
    ):
        return from_port[2]
    return None


def _ec2_all_ports_open(graph: Graph, nid: NId) -> Iterator[NId]:
    cidr = get_optional_attribute(
        graph, nid, "CidrIp"
    ) or get_optional_attribute(graph, nid, "CidrIpv6")

    if not cidr:
        return

    if (
        cidr[1] in PUBLIC_CIDRS
        and (to_port := get_optional_attribute(graph, nid, "ToPort"))
        and (from_port := get_optional_attribute(graph, nid, "FromPort"))
        and float(from_port[1]) == 0
        and float(to_port[1]) == 65535
    ):
        yield from_port[2]


def _ec2_has_sec_groups_in_rfc1918(graph: Graph, nid: NId) -> NId | None:
    rfc1918 = {"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}
    cidr = get_optional_attribute(
        graph, nid, "CidrIp"
    ) or get_optional_attribute(graph, nid, "CidrIpv6")
    if cidr and is_cidr(cidr[1]) and cidr[1] in rfc1918:
        return cidr[2]
    return None


def _unrestricted_cidrs(graph: Graph, nid: NId) -> Iterator[NId]:
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    cidr = get_optional_attribute(graph, nid, "CidrIp")
    with suppress(AddressValueError, KeyError):
        if cidr and (IPv4Network(cidr[1], strict=False) == unrestricted_ipv4):
            yield cidr[2]
    cidrv6 = get_optional_attribute(graph, nid, "CidrIpv6")
    with suppress(AddressValueError, KeyError):
        if cidrv6 and (
            IPv6Network(cidrv6[1], strict=False) == unrestricted_ipv6
        ):
            yield cidrv6[2]


def _allows_anyone_to_admin_ports(graph: Graph, nid: NId) -> Iterator[NId]:
    admin_ports = {
        22,  # SSH
        1521,  # Oracle
        1433,  # MSSQL
        1434,  # MSSQL
        2438,  # Oracle
        3306,  # MySQL
        3389,  # RDP
        5432,  # Postgres
        6379,  # Redis
        7199,  # Cassandra
        8111,  # DAX
        8888,  # Cassandra
        9160,  # Cassandra
        11211,  # Memcached
        27017,  # MongoDB
        445,  # CIFS
    }
    unrestricted_ipv4 = IPv4Network("0.0.0.0/0")
    unrestricted_ipv6 = IPv6Network("::/0")
    unrestricted_ip = False

    if (
        (to_port := get_optional_attribute(graph, nid, "ToPort"))
        and (from_port := get_optional_attribute(graph, nid, "FromPort"))
        and (port_range := set(range(int(from_port[1]), int(to_port[1]) + 1)))
    ):
        if cidr := get_optional_attribute(graph, nid, "CidrIpv6"):
            with suppress(AddressValueError, KeyError):
                unrestricted_ip = (
                    IPv6Network(cidr[1], strict=False) == unrestricted_ipv6
                )
        if cidrv4 := get_optional_attribute(graph, nid, "CidrIp"):
            with suppress(AddressValueError, KeyError):
                unrestricted_ip = (
                    IPv4Network(cidrv4[1], strict=False) == unrestricted_ipv4
                    or unrestricted_ip
                )
        if unrestricted_ip and admin_ports.intersection(port_range):
            yield from_port[2]
            yield to_port[2]


def _iterate_secgroup_traffic(
    graph: Graph,
    traffic_dir: str,
) -> Iterator[NId]:
    for nid in matching_nodes(graph, label_type="Object"):
        if (
            (resource := get_optional_attribute(graph, nid, "Type"))
            and resource[1] == traffic_dir
            and (prop := get_optional_attribute(graph, nid, "Properties"))
            and (val_id := graph.nodes[prop[2]]["value_id"])
        ):
            yield val_id


def _iterate_traffic_dir(
    graph: Graph, val_id: NId, traffic_dir: str, is_traffic_dir: bool
) -> Iterator[NId]:
    if (
        is_traffic_dir
        and (traffic := get_optional_attribute(graph, val_id, traffic_dir))
        and (traffic_attrs := graph.nodes[traffic[2]]["value_id"])
    ):
        for c_id in adj_ast(graph, traffic_attrs):
            yield c_id


def iterate_ec2_egress_ingress(
    graph: Graph,
    method_supplies: MethodSupplies,
    is_ingress: bool = False,
    is_egress: bool = False,
) -> Iterator[NId]:
    for nid in method_supplies.selected_nodes:
        resource = get_optional_attribute(graph, nid, "Type")
        if (
            resource
            and resource[1] == "AWS::EC2::SecurityGroup"
            and (prop := get_optional_attribute(graph, nid, "Properties"))
        ):
            val_id = graph.nodes[prop[2]]["value_id"]
            yield from _iterate_traffic_dir(
                graph, val_id, "SecurityGroupIngress", is_ingress
            )
            yield from _iterate_traffic_dir(
                graph, val_id, "SecurityGroupEgress", is_egress
            )
    if is_ingress:
        yield from _iterate_secgroup_traffic(
            graph, "AWS::EC2::SecurityGroupIngress"
        )
    if is_egress:
        yield from _iterate_secgroup_traffic(
            graph, "AWS::EC2::SecurityGroupEgress"
        )


def cfn_allows_anyone_to_admin_ports(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ANYONE_ADMIN_PORTS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph, method_supplies, is_ingress=True
        ):
            for report in _allows_anyone_to_admin_ports(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_allows_anyone_to_admin_ports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_unrestricted_cidrs(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_UNRESTRICTED_CIDRS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph, method_supplies, is_ingress=True
        ):
            for report in _unrestricted_cidrs(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_unrestricted_cidrs",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_security_groups_ip_ranges_in_rfc1918(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_SEC_GROUPS_RFC1918

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph, method_supplies, is_ingress=True, is_egress=True
        ):
            if report := _ec2_has_sec_groups_in_rfc1918(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f024.ec2_has_security_groups_ip_ranges_in_rfc1918"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_open_all_ports_to_the_public(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_OPEN_ALL_PORTS_PUBLIC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph, method_supplies, is_ingress=True, is_egress=True
        ):
            for report in _ec2_all_ports_open(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_open_all_ports_to_the_public",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_unrestricted_dns_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNRESTRICTED_DNS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph, method_supplies, is_ingress=True, is_egress=True
        ):
            if report := _ec2_has_unrestricted_dns_access(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_unrestricted_dns_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_unrestricted_ftp_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNRESTRICTED_FTP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph, method_supplies, is_ingress=True, is_egress=True
        ):
            for report in _ec2_has_unrestricted_ftp_access(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_unrestricted_ftp_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_ec2_has_unrestricted_ports(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_UNRESTRICTED_PORTS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph,
            method_supplies=method_supplies,
            is_ingress=True,
            is_egress=True,
        ):
            if report := _ec2_has_unrestricted_ports(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_unrestricted_ports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_unrestricted_ip_protocols(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_UNRESTRICTED_IP_PROTO

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_ec2_egress_ingress(
            graph,
            method_supplies=method_supplies,
            is_ingress=True,
            is_egress=True,
        ):
            if report := _unrestricted_ip_protocols(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_unrestricted_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_groups_without_egress(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_GROUPS_WITHOUT_EGRESS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::EC2::SecurityGroup"
                and (report := _group_without_egress(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_security_group_without_egress",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_instances_without_profile(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INST_WITHOUT_PROFILE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::EC2::Instance"
                and (report := _instances_without_profile(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_instances_without_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
