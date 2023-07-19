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
from lib.root.f024.constants import (
    ADMIN_PORTS,
    UNRESTRICTED_IPV4,
    UNRESTRICTED_IPV6,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_attribute,
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


def _ec2_instances_without_profile(graph: Graph, nid: NId) -> NId | None:
    expected_attr, _, _ = get_attribute(graph, nid, "iam_instance_profile")
    if not expected_attr:
        return nid
    return None


def _aws_ec2_allows_all_outbound_traffic(graph: Graph, nid: NId) -> NId | None:
    if not get_argument(graph, nid, "egress"):
        return nid
    return None


def _aws_allows_anyone_to_admin_ports(graph: Graph, nid: NId) -> Iterator[NId]:
    type_attr = get_attribute(graph, nid, "type")
    if type_attr[0] is None or (type_attr[0] and type_attr[1] == "ingress"):
        unrestricted_ip = False
        cidr_ip, cidr_ip_val, _ = get_attribute(graph, nid, "cidr_blocks")
        cidr_ipv6, cidr_ipv6_val, _ = get_attribute(
            graph, nid, "ipv6_cidr_blocks"
        )
        with suppress(AddressValueError, KeyError):
            unrestricted_ip = (
                cidr_ipv6 is not None
                and IPv6Network(
                    cidr_ipv6_val,
                    strict=False,
                )
                == UNRESTRICTED_IPV6
            )
        with suppress(AddressValueError, KeyError):
            unrestricted_ip = (
                IPv4Network(
                    cidr_ip_val,
                    strict=False,
                )
                == UNRESTRICTED_IPV4
                if cidr_ip
                else unrestricted_ip
            ) or unrestricted_ip
        from_port, from_port_val, from_port_id = get_attribute(
            graph, nid, "from_port"
        )
        to_port, to_port_val, to_port_id = get_attribute(graph, nid, "to_port")
        port_range = (
            set(
                range(
                    int(from_port_val),
                    int(to_port_val) + 1,
                )
            )
            if from_port and to_port
            else set()
        )
        if unrestricted_ip and ADMIN_PORTS.intersection(port_range):
            yield from_port_id
            yield to_port_id


def _aux_ec2_has_unrestricted_ports(graph: Graph, nid: NId) -> Iterator[NId]:
    from_port, from_port_val, _ = get_attribute(graph, nid, "from_port")
    to_port, to_port_val, _ = get_attribute(graph, nid, "to_port")
    if from_port and to_port and float(from_port_val) != float(to_port_val):
        yield nid


def _ec2_has_unrestricted_ports(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_security_group":
        if ingress := get_argument(graph, nid, "ingress"):
            yield from _aux_ec2_has_unrestricted_ports(graph, ingress)
        if egress := get_argument(graph, nid, "egress"):
            yield from _aux_ec2_has_unrestricted_ports(graph, egress)
    elif graph.nodes[nid]["name"] == "aws_security_group_rule":
        yield from _aux_ec2_has_unrestricted_ports(graph, nid)


def aux_aws_ec2_cfn_unrestricted_ip_protocols(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    danger_values = ("-1", -1)
    protocol, protocol_val, p_id = get_attribute(graph, nid, "protocol")
    if protocol and protocol_val in danger_values:
        yield p_id


def _aws_ec2_cfn_unrestricted_ip_protocols(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_security_group":
        if ingress := get_argument(graph, nid, "ingress"):
            yield from aux_aws_ec2_cfn_unrestricted_ip_protocols(
                graph, ingress
            )
        if egress := get_argument(graph, nid, "egress"):
            yield from aux_aws_ec2_cfn_unrestricted_ip_protocols(graph, egress)
    elif graph.nodes[nid]["name"] == "aws_security_group_rule":
        yield from aux_aws_ec2_cfn_unrestricted_ip_protocols(graph, nid)


def _ec2_unrestricted_cidrs(
    ip_val: str, ip_type: str, rule: str | None = None
) -> bool:
    with suppress(AddressValueError, KeyError):
        if ip_type == "ipv4":
            ipv4_object = IPv4Network(ip_val, strict=False)
            if ipv4_object == UNRESTRICTED_IPV4 or (
                rule == "ingress" and ipv4_object.num_addresses > 1
            ):
                return True
        else:
            ipv6_object = IPv6Network(ip_val, strict=False)
            if ipv6_object == UNRESTRICTED_IPV6 or (
                rule == "ingress" and ipv6_object.num_addresses > 1
            ):
                return True
    return False


def _aux_ingress_unrestricted_cidrs(graph: Graph, nid: NId) -> Iterator[NId]:
    ipv4, ipv4_val, ipv4_id = get_attribute(graph, nid, "cidr_blocks")
    if ipv4 and _ec2_unrestricted_cidrs(ipv4_val, "ipv4"):
        yield ipv4_id
    ipv6, ipv6_val, ipv6_id = get_attribute(graph, nid, "ipv6_cidr_blocks")
    if ipv6 and _ec2_unrestricted_cidrs(ipv6_val, "ipv6"):
        yield ipv6_id


def _aws_ec2_unrestricted_cidrs(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_security_group":
        if ingress := get_argument(graph, nid, "ingress"):
            yield from _aux_ingress_unrestricted_cidrs(graph, ingress)
    elif graph.nodes[nid]["name"] == "aws_security_group_rule":
        yield from _aux_ingress_unrestricted_cidrs(graph, nid)


def _ec2_has_security_groups_ip_ranges_in_rfc1918(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    rfc1918 = {
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
    }
    cidr, cidr_val, cidr_id = get_attribute(graph, nid, "cidr_blocks")
    if not cidr:
        cidr, cidr_val, cidr_id = get_attribute(graph, nid, "ipv6_cidr_blocks")
    if cidr_id:
        cidr_vals = set(cidr_val if isinstance(cidr_val, list) else [cidr_val])
        valid_cidrs = filter(is_cidr, cidr_vals)
        if rfc1918.intersection(valid_cidrs):
            yield cidr_id


def _ec2_has_unrestricted_dns_access(graph: Graph, nid: NId) -> Iterator[NId]:
    public_cidrs = {
        "::/0",
        "0.0.0.0/0",
    }
    cidr, cidr_val, cidr_id = get_attribute(graph, nid, "cidr_blocks")
    if not cidr:
        cidr, cidr_val, cidr_id = get_attribute(graph, nid, "ipv6_cidr_blocks")
    if cidr_id:
        cidr_vals = set(cidr_val if isinstance(cidr_val, list) else [cidr_val])
        valid_cidrs = filter(is_cidr, cidr_vals)
        from_port, from_port_val, from_port_id = get_attribute(
            graph, nid, "from_port"
        )
        to_port, to_port_val, _ = get_attribute(graph, nid, "to_port")
        port_range = (
            set(
                range(
                    int(from_port_val),
                    int(to_port_val) + 1,
                )
            )
            if from_port and to_port
            else set()
        )
        if public_cidrs.intersection(valid_cidrs) and 53 in port_range:
            yield from_port_id


def _ec2_has_unrestricted_ftp_access(graph: Graph, nid: NId) -> Iterator[NId]:
    public_cidrs = {
        "::/0",
        "0.0.0.0/0",
    }
    cidr, cidr_val, cidr_id = get_attribute(graph, nid, "cidr_blocks")
    if not cidr:
        cidr, cidr_val, cidr_id = get_attribute(graph, nid, "ipv6_cidr_blocks")
    if cidr_id:
        cidr_vals = set(cidr_val if isinstance(cidr_val, list) else [cidr_val])
        valid_cidrs = filter(is_cidr, cidr_vals)
        from_port, from_port_val, from_port_id = get_attribute(
            graph, nid, "from_port"
        )
        to_port, to_port_val, _ = get_attribute(graph, nid, "to_port")
        port_range = (
            set(
                range(
                    int(from_port_val),
                    int(to_port_val) + 1,
                )
            )
            if from_port and to_port
            else set()
        )
        ftp_range = set(range(20, 22))
        if public_cidrs.intersection(valid_cidrs) and port_range.intersection(
            ftp_range
        ):
            yield from_port_id


def _ec2_has_open_all_ports_to_the_public(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    public_cidrs = {
        "::/0",
        "0.0.0.0/0",
    }
    cidr, cidr_val, cidr_id = get_attribute(graph, nid, "cidr_blocks")
    if not cidr:
        cidr, cidr_val, cidr_id = get_attribute(graph, nid, "ipv6_cidr_blocks")
    if cidr_id:
        cidr_vals = set(cidr_val if isinstance(cidr_val, list) else [cidr_val])
        valid_cidrs = filter(is_cidr, cidr_vals)
        from_port, from_port_val, from_port_id = get_attribute(
            graph, nid, "from_port"
        )
        to_port, to_port_val, _ = get_attribute(graph, nid, "to_port")

        if (
            from_port
            and to_port
            and public_cidrs.intersection(valid_cidrs)
            and (int(to_port_val) - int(from_port_val)) >= 65535
        ):
            yield from_port_id


def tfm_ec2_has_open_all_ports_to_the_public(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_OPEN_ALL_PORTS_PUBLIC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
                "ingress",
                "egress",
            }:
                for report in _ec2_has_open_all_ports_to_the_public(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_open_all_ports_to_the_public",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_unrestricted_ftp_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_UNRESTRICTED_FTP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
                "ingress",
                "egress",
            }:
                for report in _ec2_has_unrestricted_ftp_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_unrestricted_ftp_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_unrestricted_dns_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_UNRESTRICTED_DNS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
                "ingress",
                "egress",
            }:
                for report in _ec2_has_unrestricted_dns_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_unrestricted_dns_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_security_groups_ip_ranges_in_rfc1918(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_SEC_GROUPS_RFC1918

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
                "ingress",
                "egress",
            }:
                for report in _ec2_has_security_groups_ip_ranges_in_rfc1918(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f024.ec2_has_security_groups_ip_ranges_in_rfc1918"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_ec2_unrestricted_cidrs(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EC2_UNRESTRICTED_CIDRS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
            }:
                for report in _aws_ec2_unrestricted_cidrs(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_unrestricted_cidrs",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_ec2_cfn_unrestricted_ip_protocols(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EC2_CFN_UNRESTR_IP_PROT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
            }:
                for report in _aws_ec2_cfn_unrestricted_ip_protocols(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_unrestricted_protocols",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_has_unrestricted_ports(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_EC2_UNRESTRICTED_PORTS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
            }:
                for report in _ec2_has_unrestricted_ports(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.ec2_has_unrestricted_ports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_allows_anyone_to_admin_ports(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ANYONE_ADMIN_PORTS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_security_group",
                "aws_security_group_rule",
                "ingress",
            }:
                for report in _aws_allows_anyone_to_admin_ports(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_allows_anyone_to_admin_ports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_ec2_instances_without_profile(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_INST_WITHOUT_PROFILE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_instance" and (
                report := _ec2_instances_without_profile(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_instances_without_profile",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_aws_ec2_allows_all_outbound_traffic(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_EC2_ALL_TRAFFIC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_security_group" and (
                report := _aws_ec2_allows_all_outbound_traffic(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f024.aws_security_group_without_egress",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
