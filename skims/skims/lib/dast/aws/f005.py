import ast
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


async def allows_priv_escalation_by_policies_versions(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    method = core.MethodsEnum.AWS_ALLOWS_PRIV_ESCALATION_BY_POLICIES_VERSIONS
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

            for index, stm in enumerate(policy_statements):
                with suppress(KeyError):
                    vulnerable = (
                        stm["Effect"] == "Allow"
                        and "Resource" in stm
                        and "iam:CreatePolicyVersion" in stm["Action"]
                        and "iam:SetDefaultPolicyVersion" in stm["Action"]
                    )

                    if vulnerable:
                        locations = [
                            *[
                                Location(
                                    access_patterns=("/Document",),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Resource"],
                                        policy_statements[index]["Action"],
                                    ),
                                    description=t(
                                        "f005.allows_priv_escalation_by_"
                                        "policies_versions"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=policy_names,
                ),
            )

    return vulns


async def allows_priv_escalation_by_attach_policy(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_policies",
        parameters={"Scope": "Local", "OnlyAttached": True},
    )
    policies = response.get("Policies", []) if response else []
    method = core.MethodsEnum.AWS_ALLOWS_PRIV_ESCALATION_BY_ATTACH_POLICY
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

            for index, stm in enumerate(policy_statements):
                with suppress(KeyError):
                    vulnerable = (
                        stm["Effect"] == "Allow"
                        and "Resource" in stm
                        and "iam:AttachUserPolicy" in stm["Action"]
                    )

                    if vulnerable:
                        locations = [
                            *[
                                Location(
                                    access_patterns=("/Document",),
                                    arn=(f"{policy['Arn']}"),
                                    values=(
                                        policy_statements[index]["Effect"],
                                        policy_statements[index]["Resource"],
                                        policy_statements[index]["Action"],
                                    ),
                                    description=t(
                                        "f005.allows_priv_escalation_by_"
                                        "attach_policy"
                                    ),
                                )
                            ],
                        ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=method,
                    aws_response=policy_names,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    allows_priv_escalation_by_policies_versions,
    allows_priv_escalation_by_attach_policy,
)
