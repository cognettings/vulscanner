from collections.abc import (
    Callable,
    Coroutine,
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


async def not_requires_uppercase(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if password_policy and not password_policy.get(
        "RequireUppercaseCharacters", False
    ):
        locations = [
            Location(
                access_patterns=("/RequireUppercaseCharacters",)
                if password_policy.get("RequireUppercaseCharacters", "")
                is False
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["RequireUppercaseCharacters"],)
                if password_policy.get("RequireUppercaseCharacters", "")
                is False
                else (),
                description=t("f363.not_requires_uppercase"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_IAM_NOT_REQUIRES_UPPERCASE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def not_requires_lowercase(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if password_policy and not password_policy.get(
        "RequireLowercaseCharacters", False
    ):
        locations = [
            Location(
                access_patterns=("/RequireLowercaseCharacters",)
                if password_policy.get("RequireLowercaseCharacters", "")
                is False
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["RequireLowercaseCharacters"],)
                if password_policy.get("RequireLowercaseCharacters", "")
                is False
                else (),
                description=t("f363.not_requires_lowercase"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_IAM_NOT_REQUIRES_LOWERCASE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def not_requires_symbols(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if password_policy and not password_policy.get("RequireSymbols", False):
        locations = [
            Location(
                access_patterns=("/RequireSymbols",)
                if password_policy.get("RequireSymbols", "") is False
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["RequireSymbols"],)
                if password_policy.get("RequireSymbols", "") is False
                else (),
                description=t("f363.not_requires_symbols"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_IAM_NOT_REQUIRES_SYMBOLS),
                aws_response=password_policy,
            ),
        )

    return vulns


async def not_requires_numbers(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if password_policy and not password_policy.get("RequireNumbers", False):
        locations = [
            Location(
                access_patterns=("/RequireNumbers",)
                if password_policy.get("RequireNumbers", "") is False
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["RequireNumbers"],)
                if password_policy.get("RequireNumbers", "") is False
                else (),
                description=t("f363.not_requires_numbers"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_IAM_NOT_REQUIRES_NUMBERS),
                aws_response=password_policy,
            ),
        )

    return vulns


async def min_password_len_unsafe(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    min_length: int = 14
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    if (
        password_policy
        and password_policy.get("MinimumPasswordLength", 0) < min_length
    ):
        locations = [
            Location(
                access_patterns=("/MinimumPasswordLength",)
                if password_policy.get("MinimumPasswordLength", "")
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["MinimumPasswordLength"],)
                if password_policy.get("MinimumPasswordLength", "")
                else (),
                description=t("f363.min_password_len_unsafe"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_MIN_PASSWORD_LEN_UNSAFE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def password_reuse_unsafe(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    password_policy = response.get("PasswordPolicy", {})
    password_reuse: int = password_policy.get("PasswordReusePrevention", 0)
    min_reuse = 24
    if password_policy and password_reuse < min_reuse:
        locations = [
            Location(
                access_patterns=("/PasswordReusePrevention",)
                if password_policy.get("PasswordReusePrevention", "")
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["PasswordReusePrevention"],)
                if password_policy.get("PasswordReusePrevention", "")
                else (),
                description=t("f363.password_reuse_unsafe"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=(core.MethodsEnum.AWS_IAM_PASSWORD_REUSE_UNSAFE),
                aws_response=password_policy,
            ),
        )

    return vulns


async def password_expiration_unsafe(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_account_password_policy"
    )
    user = await run_boto3_fun(credentials, service="iam", function="get_user")
    vulns: core.Vulnerabilities = ()
    method = core.MethodsEnum.AWS_IAM_PASSWORD_EXPIRATION_UNSAFE
    password_policy = response.get("PasswordPolicy", {})
    max_days = 90
    pasword_max_age: int = password_policy.get("MaxPasswordAge", max_days + 1)
    if password_policy and pasword_max_age > max_days:
        locations = [
            Location(
                access_patterns=("/MaxPasswordAge",)
                if password_policy.get("MaxPasswordAge", "")
                else (),
                arn=(
                    user["User"]["Arn"]  # type: ignore
                    if user.get("User", "")
                    else "arn:aws:iam:::user/#CantRecoverUser"
                ),
                values=(password_policy["MaxPasswordAge"],)
                if password_policy.get("MaxPasswordAge", "")
                else (),
                description=t("f363.password_expiration_unsafe"),
            ),
        ]

        vulns = (
            *vulns,
            *build_vulnerabilities(
                locations=locations,
                method=method,
                aws_response=password_policy,
            ),
        )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    not_requires_uppercase,
    not_requires_lowercase,
    not_requires_symbols,
    not_requires_numbers,
    min_password_len_unsafe,
    password_reuse_unsafe,
    password_expiration_unsafe,
)
