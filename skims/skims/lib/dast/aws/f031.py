import ast
import boto3
import botocore
from botocore import (
    UNSIGNED,
)
from botocore.client import (
    Config,
)
from collections.abc import (
    Callable,
    Coroutine,
)
from contextlib import (
    suppress,
)
import json
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
import re
from typing import (
    Any,
)
from utils.logs import (
    log_exception_blocking,
)
from zone import (
    t,
)


async def admin_policy_attached(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_policies"
    )
    policies = response.get("Policies", []) if response else []
    elevated_policies = {
        "arn:aws:iam::aws:policy/PowerUserAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
        "arn:aws:iam::aws:policy/AdministratorAccess",
    }
    vulns: core.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: list[Location] = []
            if (
                policy["Arn"] in elevated_policies
                and policy["AttachmentCount"] != 0
            ):
                locations = [
                    *[
                        Location(
                            access_patterns=("/Arn", "/AttachmentCount"),
                            arn=(
                                f"{policy['Arn']}: "
                                f"AttachmentCount/{policy['AttachmentCount']}"
                            ),
                            values=(
                                policy["Arn"],
                                policy["AttachmentCount"],
                            ),
                            description=t(
                                "src.lib_path.f031_aws.permissive_policy"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_ADMIN_POLICY_ATTACHED),
                    aws_response=policy,
                ),
            )

    return vulns


async def bucket_objects_can_be_listed(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []
    s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    vulns: core.Vulnerabilities = ()
    for bucket in buckets:
        try:
            nice = s3_client.list_objects_v2(Bucket=bucket["Name"], MaxKeys=10)
            if nice:
                locations = [
                    *[
                        Location(
                            access_patterns=("/Name",),
                            arn=(f"arn:aws:s3:::{bucket['Name']}"),
                            values=(bucket["Name"],),
                            description=t(
                                "src.lib_path.f031."
                                "iam_group_missing_role_based_security"
                            ),
                        )
                    ],
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=(core.MethodsEnum.AWS_PUBLIC_BUCKETS),
                        aws_response=bucket,
                    ),
                )
        except botocore.exceptions.ClientError:
            log_exception_blocking(
                "exception", botocore.exceptions.ClientError
            )
    return vulns


async def public_buckets(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []

    perms = ["READ", "WRITE", "FULL_CONTROL", "READ_ACP", "WRITE_ACP"]
    public_acl = "http://acs.amazonaws.com/groups/global/AllUsers"
    vulns: core.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            locations: list[Location] = []
            bucket_name = bucket["Name"]
            bucket_grants: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_bucket_acl",
                parameters={"Bucket": str(bucket_name)},
            )
            grants = bucket_grants.get("Grants", [])
            for index, grant in enumerate(grants):
                locations = [
                    *[
                        Location(
                            access_patterns=(f"/Grants/{index}/Permission",),
                            arn=(f"arn:aws:s3:::{bucket_name}"),
                            values=(grant["Permission"],),
                            description=t(
                                "src.lib_path.f031."
                                "bucket_policy_allows_public_access"
                            ),
                        )
                        for (key, val) in grant.items()
                        if key == "Permission"
                        and any(perm in val for perm in perms)
                        for (grantee_k, _) in grant["Grantee"].items()
                        if (
                            "URI" in grantee_k
                            and grant["Grantee"]["URI"] == public_acl
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_PUBLIC_BUCKETS),
                    aws_response=bucket_grants,
                ),
            )

    return vulns


async def group_with_inline_policies(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_groups"
    )
    groups = response.get("Groups", []) if response else []

    vulns: core.Vulnerabilities = ()
    if groups:
        for group in groups:
            group_policies: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_group_policies",
                parameters={"GroupName": str(group["GroupName"])},
            )
            policy_names = group_policies.get("PolicyNames", [])

            locations: list[Location] = []
            if policy_names:
                locations = [
                    *[
                        Location(
                            access_patterns=("/PolicyNames",),
                            arn=(f"{group['Arn']}"),
                            values=(policy_names[0],),
                            description=t(
                                "src.lib_path.f031."
                                "iam_group_missing_role_based_security"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_GROUP_WITH_INLINE_POLICY),
                    aws_response=group_policies,
                ),
            )

    return vulns


async def user_with_inline_policies(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_users"
    )
    users = response.get("Users", []) if response else []

    vulns: core.Vulnerabilities = ()
    if users:
        for user in users:
            user_policies: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_user_policies",
                parameters={"UserName": str(user["UserName"])},
            )

            policy_names = user_policies.get("PolicyNames", [])

            locations: list[Location] = []
            if policy_names:
                locations = [
                    *[
                        Location(
                            access_patterns=("/PolicyNames",),
                            arn=(f"{user['Arn']}"),
                            values=(policy_names[0],),
                            description=t(
                                "src.lib_path.f031."
                                "iam_user_missing_role_based_security"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_USER_WITH_INLINE_POLICY),
                    aws_response=user_policies,
                ),
            )

    return vulns


async def policies_attached_to_users(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_users"
    )
    users = response.get("Users", []) if response else []

    vulns: core.Vulnerabilities = ()
    if users:
        for user in users:
            user_policies: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_attached_user_policies",
                parameters={"UserName": str(user["UserName"])},
            )
            attached_policies = user_policies.get("AttachedPolicies", [])

            locations: list[Location] = []
            if attached_policies:
                locations = [
                    *[
                        Location(
                            access_patterns=("/AttachedPolicies",),
                            arn=(f"{user['Arn']}"),
                            values=(attached_policies,),
                            description=t(
                                "src.lib_path.f031.policies_attached_to_users"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_POLICIES_ATTACHED_TO_USERS),
                    aws_response=user_policies,
                ),
            )

    return vulns


async def full_access_policies(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []

    vulns: core.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: list[Location] = []
            pol_ver: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, list):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    if (
                        item["Effect"] == "Allow"
                        and item["Action"] == "*"
                        and item["Resource"] == "*"
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Statement/{index}/Effect",
                                        f"/Statement/{index}/Action",
                                        f"/Statement/{index}/Resource",
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Action"],
                                        policy_statements[index]["Resource"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031_aws.permissive_policy"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_FULL_ACCESS_POLICIES),
                    aws_response=pol_access,
                ),
            )

    return vulns


def _match_pattern(pattern: str, target: str, flags: int = 0) -> bool:
    # Escape everything that is not `*` and replace `*` with regex `.*`
    pattern = r".*".join(map(re.escape, pattern.split("*")))
    return bool(re.match(f"^{pattern}$", target, flags=flags))


def _match_iam_passrole(action: str) -> bool:
    return _match_pattern(str(action), "iam:PassRole")


def _get_action(item: dict, value: str) -> list | str:
    if isinstance(item[value], str):
        return [item[value]]
    return item[value]


async def open_passrole(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []

    vulns: core.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: list[Location] = []
            pol_ver: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, list):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    action = _get_action(item, "Action")

                    if (
                        item["Effect"] == "Allow"
                        and any(map(_match_iam_passrole, action))
                        and item["Resource"] == "*"
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Statement/{index}/Effect",
                                        f"/Statement/{index}/Action",
                                        f"/Statement/{index}/Resource",
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Action"],
                                        policy_statements[index]["Resource"],
                                    ),
                                    description=t(
                                        "src.lib_path.f031_aws.open_passrole"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_OPEN_PASSROLE),
                    aws_response=pol_access,
                ),
            )

    return vulns


def _is_action_permissive(action: Any) -> bool:
    if not isinstance(action, str):
        # A var or syntax error
        return False

    splitted = action.split(":", 1)  # a:b
    provider = splitted[0]  # a
    effect = splitted[1] if splitted[1:] else None  # b

    return (
        (provider == "*")
        or (effect and effect.startswith("*"))
        or ("*" in provider and effect is None)
    )


async def permissive_policy(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    vulns: core.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: list[Location] = []
            pol_ver: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, list):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    action = _get_action(item, "Action")

                    if (
                        item["Effect"] == "Allow"
                        and any(map(_is_action_permissive, action))
                        and item["Resource"] == "*"
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Statement/{index}/Action",
                                        f"/Statement/{index}/Resource",
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Action"],
                                        policy_statements[index]["Resource"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031_aws.permissive_policy"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_PERMISSIVE_POLICY),
                    aws_response=pol_access,
                ),
            )

    return vulns


async def has_permissive_role_policies(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_roles",
    )
    roles = response.get("Roles", []) if response else []
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_HAS_PERMISSIVE_ROLE_POLICY

    async def get_role_policies(role_name: str) -> list:
        response = await run_boto3_fun(
            credentials,
            service="iam",
            function="list_role_policies",
            parameters={"RoleName": role_name},
        )
        return list(response["PolicyNames"]) if response else []

    async def get_policy_role(
        policy_name: str, role_name: str
    ) -> dict[str, str]:
        response = await run_boto3_fun(
            credentials,
            service="iam",
            function="get_role_policy",
            parameters={"PolicyName": policy_name, "RoleName": role_name},
        )
        return dict(response["PolicyDocument"])

    for role in roles:
        locations: list[Location] = []
        role_policies = await get_role_policies(role["RoleName"])
        for policy_name in role_policies:
            policy_role = await get_policy_role(policy_name, role["RoleName"])
            policy_statements = ast.literal_eval(
                str(policy_role.get("Statement", []))
            )
            for index, statement in enumerate(policy_statements):
                if (
                    statement["Action"] in ("*", ["*"])
                    and statement["Effect"] == "Allow"
                ):
                    locations = [
                        *locations,
                        *[
                            Location(
                                access_patterns=(
                                    f"/{index}/Effect",
                                    f"/{index}/Action",
                                ),
                                arn=(f"{role['RoleName']}"),
                                values=(
                                    statement["Effect"],
                                    statement["Action"],
                                ),
                                description=t(
                                    "src.lib_path.f031."
                                    "has_permissive_role_policies"
                                ),
                            )
                        ],
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=policy_statements,
                ),
            )

    return vulns


async def full_access_to_ssm(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    vulns: core.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: list[Location] = []
            pol_ver: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, list):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    action = _get_action(item, "Action")

                    if item["Effect"] == "Allow" and any(
                        map(lambda act: act == "ssm:*", action)
                    ):
                        locations = [
                            *[
                                Location(
                                    access_patterns=(
                                        f"/Statement/{index}/Action",
                                    ),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Action"],
                                    ),
                                    description=t(
                                        "src.lib_path."
                                        "f031.iam_has_full_access_to_ssm"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_FULL_ACCESS_SSM),
                    aws_response=pol_access,
                ),
            )

    return vulns


def _get_locations(
    index: int,
    item: dict,
    policy: dict[str, Any],
    policy_statements: dict[int, Any],
) -> list:
    locations: list[Location] = []
    action = _get_action(item, "NotAction")

    if item["Effect"] == "Allow" and not _is_action_permissive(action):
        locations = [
            *[
                Location(
                    access_patterns=(f"/Statement/{index}/NotAction",),
                    arn=(f"{policy['Arn']}"),
                    values=policy_statements[index]["NotAction"],
                    description=t(
                        "src.lib_path.f031.iam_has_full_access_to_ssm"
                    ),
                )
            ],
        ]

    if item["Effect"] == "Allow" and item["NotResource"] != "*":
        locations = [
            *[
                Location(
                    access_patterns=(f"/Statement/{index}/NotResource",),
                    arn=(f"{policy['Arn']}"),
                    values=policy_statements[index]["NotResource"],
                    description=t("src.lib_path.f031_aws.negative_statement"),
                )
            ],
        ]
    return locations


async def negative_statement(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    vulns: core.Vulnerabilities = ()
    if policies:
        for policy in policies:
            locations: list[Location] = []
            pol_ver: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="get_policy_version",
                parameters={
                    "PolicyArn": str(policy["Arn"]),
                    "VersionId": str(policy["DefaultVersionId"]),
                },
            )
            policy_names = pol_ver.get("PolicyVersion", {})
            pol_access = ast.literal_eval(
                str(policy_names.get("Document", {}))
            )
            policy_statements = ast.literal_eval(
                str(pol_access.get("Statement", []))
            )

            if not isinstance(policy_statements, list):
                policy_statements = [policy_statements]

            for index, item in enumerate(policy_statements):
                item = ast.literal_eval(str(item))
                with suppress(KeyError):
                    locations = _get_locations(
                        index, item, policy, policy_statements
                    )

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_NEGATIVE_STATEMENT),
                    aws_response=pol_access,
                ),
            )

    return vulns


async def users_with_password_and_access_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="list_users"
    )
    users = response.get("Users", []) if response else []
    method = core.MethodsEnum.AWS_IAM_USERS_WITH_PASSWORD_AND_ACCESS_KEYS
    vulns: core.Vulnerabilities = ()
    if users:
        for user in users:
            locations = []
            access_keys: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_access_keys",
                parameters={
                    "UserName": user["UserName"],
                },
            )
            access_key_metadata = (
                access_keys["AccessKeyMetadata"] if access_keys else {}
            )
            access_keys_activated: bool = any(
                map(lambda x: x["Status"], access_key_metadata)
            )

            login_profile = None
            try:
                login_profile = await run_boto3_fun(
                    credentials,
                    service="iam",
                    function="get_login_profile",
                    parameters={"UserName": str(user["UserName"])},
                )
            except botocore.errorfactory.NoSuchEntityException:
                continue

            if access_keys_activated and login_profile:
                locations = [
                    *[
                        Location(
                            access_patterns=("/AccessKeyMetadata",),
                            arn=(f"{user['Arn']}"),
                            values=access_keys["AccessKeyMetadata"],
                            description=t(
                                "src.lib_path.f031."
                                "iam_group_missing_role_based_security"
                            ),
                        )
                    ],
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=access_keys,
                ),
            )

    return vulns


async def vpc_endpoints_exposed(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="ec2", function="describe_vpc_endpoints"
    )
    vpc_endpoints = response.get("VpcEndpoints", []) if response else []
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_VPC_ENDPOINTS_EXPOSED
    for endpoint in vpc_endpoints:
        locations: list[Location] = []
        if endpoint["VpcEndpointType"] != "Interface":
            policy_document = json.loads(endpoint["PolicyDocument"])
            for index, sts in enumerate(policy_document["Statement"]):
                if (
                    sts["Principal"] in ["*", {"AWS": "*"}]
                    and "Condition" not in sts.keys()
                ):
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    f"/Statement/{index}/Principal",
                                ),
                                arn=(
                                    f"arn:aws:ec2::VpcEndpointId:"
                                    f"{endpoint['VpcEndpointId']}"
                                ),
                                values=(sts["Principal"],),
                                description=t(
                                    "src.lib_path.f031.vpc_endpoints_exposed"
                                ),
                            )
                        ],
                    ]

                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=method,
                            aws_response=policy_document,
                        ),
                    )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    admin_policy_attached,
    full_access_policies,
    open_passrole,
    public_buckets,
    permissive_policy,
    negative_statement,
    full_access_to_ssm,
    group_with_inline_policies,
    user_with_inline_policies,
    policies_attached_to_users,
    has_permissive_role_policies,
    users_with_password_and_access_keys,
    vpc_endpoints_exposed,
)
