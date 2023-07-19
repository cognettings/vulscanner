from collections.abc import (
    Callable,
    Coroutine,
)
from contextlib import (
    suppress,
)
from lib.dast.aws.types import (
    Location,
)
from lib.dast.aws.utils import (
    build_vulnerabilities,
    run_boto3_fun,
)
from model import (
    core,
)
from model.core import (
    AwsCredentials,
    Vulnerability,
)
from typing import (
    Any,
)
from zone import (
    t,
)


def _get_security_groups(response: dict[str, Any]) -> list | Any:
    return response.get("SecurityGroups", []) if response else []


async def allows_anyone_to_admin_ports(  # NOSONAR
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    admin_ports = {
        22,  # SSH
        1521,  # Oracle
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

    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    vulns: tuple[Vulnerability, ...] = ()
    security_groups = _get_security_groups(response)
    for group in security_groups:
        locations: list[Location] = []
        for port in admin_ports:
            for index, perm in enumerate(group["IpPermissions"]):
                if "FromPort" not in perm and "ToPort" not in perm:
                    continue
                if not perm["FromPort"] <= port <= perm["ToPort"]:
                    continue
                for index_ip_range, ip_range in enumerate(perm["IpRanges"]):
                    if ip_range["CidrIp"] == "0.0.0.0/0":
                        locations = [
                            *locations,
                            Location(
                                arn=(
                                    f"arn:aws:ec2::{group['OwnerId']}:"
                                    f"security-group/{group['GroupId']}"
                                ),
                                description=t(
                                    "f024.allows_anyone_to_admin_ports",
                                    port=port,
                                ),
                                access_patterns=(
                                    f"/IpPermissions/{index}/FromPort",
                                    f"/IpPermissions/{index}/ToPort",
                                    (
                                        f"/IpPermissions/{index}/IpRanges"
                                        f"/{index_ip_range}/CidrIp"
                                    ),
                                ),
                                values=(
                                    perm["FromPort"],
                                    perm["ToPort"],
                                    ip_range["CidrIp"],
                                ),
                            ),
                        ]
                for index_ip_range, ip_range in enumerate(perm["Ipv6Ranges"]):
                    if ip_range["CidrIpv6"] == "::/0":
                        locations = [
                            *locations,
                            Location(
                                arn=(
                                    f"arn:aws:ec2::{group['OwnerId']}:"
                                    f"security-group/{group['GroupId']}"
                                ),
                                description=t(
                                    "f024.allows_anyone_to_admin_ports",
                                    port=port,
                                ),
                                access_patterns=(
                                    f"/IpPermissions/{index}/FromPort",
                                    f"/IpPermissions/{index}/ToPort",
                                    (
                                        f"/IpPermissions/{index}/Ipv6Ranges"
                                        f"/{index_ip_range}/CidrIpv6"
                                    ),
                                ),
                                values=(
                                    perm["FromPort"],
                                    perm["ToPort"],
                                    ip_range["CidrIpv6"],
                                ),
                            ),
                        ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=core.MethodsEnum.AWS_ANYONE_ADMIN_PORTS,
                aws_response=group,
            ),
        )
    return vulns


async def unrestricted_cidrs(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissions/{index_ip}/"
                                f"IpRanges/{index_range}/CidrIp"
                            ),
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(ip_range["CidrIp"],),
                        description=t("f024.aws_unrestricted_cidrs"),
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissions"]
                    )
                    for index_range, ip_range in enumerate(
                        ip_permission["IpRanges"]
                    )
                    if (ip_range.get("CidrIp") == "0.0.0.0/0")
                ],
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissions/{index_ip}/"
                                f"IpRanges/{index_range}/CidrIp"
                            ),
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(ip_range["CidrIpv6"],),
                        description=t("f024.aws_unrestricted_cidrs"),
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissions"]
                    )
                    for index_range, ip_range in enumerate(
                        ip_permission["Ipv6Ranges"]
                    )
                    if (ip_range.get("CidrIpv6") == "::/0")
                ],
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_UNRESTRICTED_CIDRS),
                    aws_response=group,
                ),
            )
    return vulns


async def unrestricted_ip_protocols(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()
    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            f"/IpPermissions/{index_ip}/FromPort",
                            f"/IpPermissions/{index_ip}/ToPort",
                            f"/IpPermissions/{index_ip}/IpProtocol",
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(
                            ip_permission.get("FromPort"),
                            ip_permission.get("ToPort"),
                            ip_permission.get("IpProtocol"),
                        ),
                        description=t("f024.aws_unrestricted_protocols"),
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissions"]
                    )
                    if ip_permission["IpProtocol"] in ("-1", -1)
                ],
            ]
            locations = [
                *locations,
                *[
                    Location(
                        access_patterns=(
                            f"/IpPermissions/{index_ip}/FromPort",
                            f"/IpPermissions/{index_ip}/ToPort",
                            f"/IpPermissionsEgress/{index_ip}/IpProtocol",
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(
                            ip_permission.get("FromPort"),
                            ip_permission.get("ToPort"),
                            ip_permission.get("IpProtocol"),
                        ),
                        description=t("f024.aws_unrestricted_protocols"),
                    )
                    for index_ip, ip_permission in enumerate(
                        group["IpPermissionsEgress"]
                    )
                    if (ip_permission["IpProtocol"] in ("-1", -1))
                ],
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_UNRESTRICTED_IP_PROTOCOlS),
                    aws_response=group,
                ),
            )
    return vulns


async def security_groups_ip_ranges_in_rfc1918(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    rfc1918 = {"10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"}
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations = [
                *[
                    Location(
                        access_patterns=(
                            (
                                f"/IpPermissions/{index}/IpRanges"
                                f"/{index_ip_range}/CidrIp"
                            ),
                        ),
                        arn=(
                            f"arn:aws:ec2::{group['OwnerId']}:"
                            f"security-group/{group['GroupId']}"
                        ),
                        values=(ip_range["CidrIp"],),
                        description=t(
                            "f024."
                            "ec2_has_security_groups_ip_ranges_in_rfc1918"
                        ),
                    )
                    for index, ip_permission in enumerate(
                        group["IpPermissions"]
                    )
                    for index_ip_range, ip_range in enumerate(
                        ip_permission["IpRanges"]
                    )
                    if ip_range["CidrIp"] in rfc1918
                ],
            ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_SEC_GROUPS_RFC1918),
                    aws_response=group,
                ),
            )
    return vulns


async def unrestricted_dns_access(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: list[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if ip_permission["FromPort"] <= 53 <= ip_permission[
                        "ToPort"
                    ] and ip_permission["IpProtocol"] in {"tcp", "udp"}:
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/IpRanges"
                                            f"/{index_ip_range}/CidrIp"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIp"],
                                    ),
                                    description=t(
                                        "f024.ec2_has_unrestricted_dns_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["IpRanges"]
                                )
                                if ip_range["CidrIp"] == "0.0.0.0/0"
                            ],
                        ]
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/"
                                            "Ipv6Ranges"
                                            f"/{index_ip_range}/CidrIpv6"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIpv6"],
                                    ),
                                    description=t(
                                        "f024."
                                        "ec2_has_unrestricted_dns_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["Ipv6Ranges"]
                                )
                                if ip_range["CidrIpv6"] == "::/0"
                            ],
                        ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_UNRESTRICTED_DNS_ACCESS),
                    aws_response=group,
                ),
            )
    return vulns


async def unrestricted_ftp_access(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: list[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if (
                        ip_permission["FromPort"]
                        <= 20
                        <= ip_permission["ToPort"]
                        and ip_permission["FromPort"]
                        <= 21
                        <= ip_permission["ToPort"]
                        and ip_permission["IpProtocol"] in {"tcp"}
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/IpRanges"
                                            f"/{index_ip_range}/CidrIp"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIp"],
                                    ),
                                    description=t(
                                        "f024.ec2_has_unrestricted_dns_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["IpRanges"]
                                )
                                if ip_range["CidrIp"] == "0.0.0.0/0"
                            ],
                        ]
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        f"/IpPermissions/{index}/FromPort",
                                        f"/IpPermissions/{index}/ToPort",
                                        (
                                            f"/IpPermissions/{index}/"
                                            "Ipv6Ranges"
                                            f"/{index_ip_range}/CidrIpv6"
                                        ),
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        ip_permission["FromPort"],
                                        ip_permission["ToPort"],
                                        ip_range["CidrIpv6"],
                                    ),
                                    description=t(
                                        "f024.ec2_has_unrestricted_ftp_access"
                                    ),
                                )
                                for index_ip_range, ip_range in enumerate(
                                    ip_permission["Ipv6Ranges"]
                                )
                                if ip_range["CidrIpv6"] == "::/0"
                            ],
                        ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_UNRESTRICTED_FTP_ACCESS),
                    aws_response=group,
                ),
            )
    return vulns


def _get_locations_permissions(
    index: int, ip_permission: dict, group: dict, locations: list[Location]
) -> list[Location]:
    if ip_permission["FromPort"] == 0 and ip_permission["ToPort"] == 65535:
        locations = [
            *[
                Location(
                    access_patterns=(
                        f"/IpPermissions/{index}/FromPort",
                        f"/IpPermissions/{index}/ToPort",
                        (
                            f"/IpPermissions/{index}/IpRanges"
                            f"/{index_ip_range}/CidrIp"
                        ),
                    ),
                    arn=(
                        f"arn:aws:ec2::{group['OwnerId']}:"
                        f"security-group/{group['GroupId']}"
                    ),
                    values=(
                        ip_permission["FromPort"],
                        ip_permission["ToPort"],
                        ip_range["CidrIp"],
                    ),
                    description=t("f024.ec2_has_open_all_ports_to_the_public"),
                )
                for index_ip_range, ip_range in enumerate(
                    ip_permission["IpRanges"]
                )
                if ip_range["CidrIp"] == "0.0.0.0/0"
            ],
        ]
    return locations


async def open_all_ports_to_the_public(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = response.get("SecurityGroups", []) if response else []
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: list[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    locations = _get_locations_permissions(
                        index, ip_permission, group, locations
                    )
            for index, ip_permission in enumerate(
                group["IpPermissionsEgress"]
            ):
                with suppress(KeyError):
                    if (
                        ip_permission["FromPort"] == 0
                        and ip_permission["ToPort"] == 65535
                    ):
                        locations = [
                            *locations,
                            Location(
                                access_patterns=(
                                    (
                                        f"/IpPermissionsEgress/{index}"
                                        "/FromPort"
                                    ),
                                    f"/IpPermissionsEgress/{index}/ToPort",
                                ),
                                arn=(
                                    f"arn:aws:ec2::{group['OwnerId']}:"
                                    f"security-group/{group['GroupId']}"
                                ),
                                values=(
                                    ip_permission["FromPort"],
                                    ip_permission["ToPort"],
                                ),
                                description=t(
                                    "f024.ec2_has_open_all_ports_to_the_public"
                                ),
                            ),
                        ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_OPEN_ALL_PORTS_TO_THE_PUBLIC),
                    aws_response=group,
                ),
            )
    return vulns


async def default_seggroup_allows_all_traffic(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            if group["GroupName"] != "default":
                continue
            locations: list[Location] = []
            for index, ip_permission in enumerate(group["IpPermissions"]):
                locations = [
                    *[
                        Location(
                            access_patterns=(
                                (
                                    f"/IpPermissions/{index}/IpRanges"
                                    f"/{index_ip_range}/CidrIp"
                                ),
                            ),
                            arn=(
                                f"arn:aws:ec2::{group['OwnerId']}:"
                                f"security-group/{group['GroupId']}"
                            ),
                            values=(ip_range["CidrIp"],),
                            description=t(
                                "f024.default_seggroup_allows_all_traffic"
                            ),
                        )
                        for index_ip_range, ip_range in enumerate(
                            ip_permission["IpRanges"]
                        )
                        if ip_range["CidrIp"] == "0.0.0.0/0"
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_DEFAULT_ALL_TRAFIC),
                    aws_response=group,
                ),
            )
    return vulns


async def instances_without_profile(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_instances"
    )
    instances = response.get("Reservations", []) if response else []
    vulns: core.Vulnerabilities = ()

    for i in instances:
        locations: list[Location] = []
        for config in i["Instances"]:
            if (
                "IamInstanceProfile" not in config.keys()
                and config["State"]["Name"] != "terminated"
            ):
                locations = [
                    *locations,
                    *[
                        Location(
                            arn=(
                                f"arn:aws:ec2::{i['OwnerId']}:"
                                f"instance-id/{config['InstanceId']}"
                            ),
                            description=t(
                                "f024.aws_instances_without_profile"
                            ),
                            values=(),
                            access_patterns=(),
                        )
                    ],
                ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_INSTANCES_WITHOUT_PROFILE),
                aws_response=i,
            ),
        )
    return vulns


async def insecure_port_range_in_security_group(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_security_groups"
    )
    security_groups = _get_security_groups(response)
    vulns: core.Vulnerabilities = ()

    if security_groups:
        for group in security_groups:
            locations: list[Location] = []
            for index, rule in enumerate(group["IpPermissions"]):
                with suppress(KeyError):
                    if rule["FromPort"] != rule["ToPort"]:
                        locations = [
                            *locations,
                            *[
                                Location(
                                    access_patterns=(
                                        (
                                            f"/IpPermissions/{index}"
                                            "/FromPort"
                                        ),
                                        f"/IpPermissions/{index}/ToPort",
                                    ),
                                    arn=(
                                        f"arn:aws:ec2::{group['OwnerId']}:"
                                        f"security-group/{group['GroupId']}"
                                    ),
                                    values=(
                                        rule["FromPort"],
                                        rule["ToPort"],
                                    ),
                                    description=t(
                                        "f024.ec2_has_unrestricted_ports"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_INSECURE_PORT_RANGE),
                    aws_response=group,
                ),
            )
    return vulns


def _acl_rule_is_public(acl_rule: dict, egress: bool, action: str) -> bool:
    """Check if an ACL rule allow all ingress traffic."""
    is_public = False
    if acl_rule["Egress"] == egress and acl_rule["RuleAction"] == action:
        if "CidrBlock" in acl_rule.keys():
            is_public = acl_rule["CidrBlock"] == "0.0.0.0/0"
        if "Ipv6CidrBlock" in acl_rule.keys():
            is_public = acl_rule["Ipv6CidrBlock"] == "::/0"
    return (
        is_public
        and "PortRange" not in acl_rule.keys()
        and acl_rule["Protocol"] == "-1"
    )


async def network_acls_allow_all_ingress_traffic(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_network_acls"
    )
    method = core.MethodsEnum.AWS_ACL_ALLOW_ALL_INGRESS_TRAFFIC
    network_acls = response.get("NetworkAcls", []) if response else []
    vulns: core.Vulnerabilities = ()
    locations: list[Location] = []

    if network_acls:
        for rule in network_acls:
            for entry in rule["Entries"]:
                if (
                    not entry["Egress"]
                    and _acl_rule_is_public(entry, False, "allow")
                    and entry.get("CidrBlock", "")
                ):
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    "/Egress",
                                    "/CidrBlock",
                                    "/Protocol",
                                ),
                                arn=(
                                    "arn:aws:vpc:networkAclId:"
                                    f"{rule['NetworkAclId']}:"
                                ),
                                values=(
                                    entry["Egress"],
                                    entry["CidrBlock"],
                                    entry["Protocol"],
                                ),
                                description=t(
                                    "f024.network_acls_"
                                    "allow_all_ingress_traffic"
                                ),
                            )
                        ],
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=method,
                            aws_response=entry,
                        ),
                    )
                elif (
                    not entry["Egress"]
                    and _acl_rule_is_public(entry, False, "allow")
                    and entry.get("Ipv6CidrBlock", "")
                ):
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    "/Egress",
                                    "/Ipv6CidrBlock",
                                    "/Protocol",
                                ),
                                arn=(
                                    "arn:aws:vpc:networkAclId:"
                                    f"{rule['NetworkAclId']}:"
                                ),
                                values=(
                                    entry["Egress"],
                                    entry["Ipv6CidrBlock"],
                                    entry["Protocol"],
                                ),
                                description=t(
                                    "f024.network_acls_"
                                    "allow_all_ingress_traffic"
                                ),
                            )
                        ],
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=method,
                            aws_response=entry,
                        ),
                    )
    return vulns


def _acl_check_ports(acl_rule: dict) -> bool:
    vuln_port = False
    if "PortRange" not in acl_rule.keys():
        if (
            acl_rule["RuleAction"] == "allow"
            and acl_rule["Protocol"] == "-1"
            and acl_rule["Egress"]
        ) or (acl_rule["Egress"] and acl_rule["RuleAction"] == "allow"):
            vuln_port = True
    else:
        if (
            (
                int(acl_rule["PortRange"]["To"])
                - int(acl_rule["PortRange"]["From"])
                == 0
                or acl_rule["Protocol"] == "-1"
            )
            and acl_rule["RuleAction"] == "allow"
            and acl_rule["Egress"]
        ):
            vuln_port = True
    return vuln_port


def iterate_acls_allow_all_egress_traffic(
    entry: dict[str, Any],
    rule: dict[str, Any],
    vulns: core.Vulnerabilities,
) -> core.Vulnerabilities:
    locations: list[Location] = []
    method = core.MethodsEnum.AWS_ACL_ALLOW_EGRESS_TRAFFIC
    if _acl_check_ports(entry):
        locations = [
            Location(
                access_patterns=(
                    "/Egress",
                    "/Protocol",
                )
                if entry["Protocol"] == "-1"
                else (
                    "/Egress",
                    "/PortRange",
                ),
                arn=(f"arn:aws:vpc:networkAclId:{rule['NetworkAclId']}:"),
                values=(
                    entry["Egress"],
                    entry["Protocol"],
                )
                if entry["Protocol"] == "-1"
                else (
                    entry["Egress"],
                    entry["PortRange"],
                ),
                description=t("f024.network_acls_allow_egress_traffic"),
            )
        ]
        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=method,
                aws_response=entry,
            ),
        )
    return vulns


async def network_acls_allow_all_egress_traffic(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_network_acls"
    )
    network_acls = response.get("NetworkAcls", []) if response else []
    vulns: core.Vulnerabilities = ()
    if network_acls:
        for rule in network_acls:
            for entry in rule["Entries"]:
                vulns = iterate_acls_allow_all_egress_traffic(
                    entry, rule, vulns
                )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    allows_anyone_to_admin_ports,
    unrestricted_cidrs,
    unrestricted_ip_protocols,
    security_groups_ip_ranges_in_rfc1918,
    unrestricted_dns_access,
    unrestricted_ftp_access,
    open_all_ports_to_the_public,
    default_seggroup_allows_all_traffic,
    instances_without_profile,
    insecure_port_range_in_security_group,
    network_acls_allow_all_ingress_traffic,
    network_acls_allow_all_egress_traffic,
)
