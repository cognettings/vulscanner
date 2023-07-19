from collections.abc import (
    Callable,
    Coroutine,
)
from contextlib import (
    suppress,
)
import csv
from datetime import (
    datetime,
    timedelta,
)
from dateutil import (
    parser,
)
from io import (
    StringIO,
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
import pytz
from typing import (
    Any,
)
from zone import (
    t,
)


async def has_old_ssh_public_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_IAM_HAS_OLD_SSH_PUBLIC_KEYS
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="list_users",
    )
    vulns: core.Vulnerabilities = ()
    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)
    users = response.get("Users", [])

    if users:
        for user in users:
            access_keys: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_ssh_public_keys",
                parameters={
                    "UserName": user["UserName"],
                },
            )
            keys = access_keys["SSHPublicKeys"] if access_keys else {}
            locations: list[Location] = []
            for index, key in enumerate(keys):
                if key["UploadDate"] < three_months_ago:
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(f"/{index}/UploadDate",),
                            arn=(f"arn:aws:iam:::{user['UserName']}"),
                            values=(keys[index]["UploadDate"],),
                            description=t(
                                "src.lib_path.f277.has_old_ssh_public_keys"
                            ),
                        ),
                    ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=keys,
                ),
            )

    return vulns


async def have_old_creds_enabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)
    vulns: core.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))
    for user in credentials_report:
        if user["password_enabled"] != "true":
            continue

        get_user: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="iam",
            function="get_user",
            parameters={"UserName": user["user"]},
        )
        with suppress(KeyError):
            user_pass_last_used = get_user["User"]["PasswordLastUsed"]
            user_arn = user["arn"]
            vulnerable = user_pass_last_used < three_months_ago
            locations: list[Location] = []
            if vulnerable:
                locations = [
                    Location(
                        access_patterns=("/User/PasswordLastUsed",),
                        arn=(f"{user_arn}"),
                        values=(user_pass_last_used,),
                        description=t(
                            "src.lib_path.f277.have_old_creds_enabled"
                        ),
                    ),
                ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_IAM_HAS_OLD_CREDS_ENABLED),
                    aws_response=get_user,
                ),
            )

    return vulns


async def have_old_access_keys(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    await run_boto3_fun(
        credentials, service="iam", function="generate_credential_report"
    )
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="iam", function="get_credential_report"
    )

    three_months_ago = datetime.now() - timedelta(days=90)
    three_months_ago = three_months_ago.replace(tzinfo=pytz.UTC)
    vulns: core.Vulnerabilities = ()
    users_csv = StringIO(response.get("Content", b"").decode())
    credentials_report = tuple(csv.DictReader(users_csv, delimiter=","))

    for user in credentials_report:
        locations: list[Location] = []
        if any(
            (
                user["access_key_1_active"] != "true",
                user["access_key_2_active"] != "true",
            )
        ):
            continue

        key_names = ("access_key_1_last_rotated", "access_key_2_last_rotated")
        with suppress(KeyError):
            for index, name in enumerate(key_names):
                if (
                    parser.parse(user[name]).replace(tzinfo=pytz.UTC)
                    < three_months_ago
                ):
                    user_arn = user["arn"]
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(f"/{key_names[index]}",),
                            arn=(f"{user_arn}"),
                            values=(user[key_names[index]],),
                            description=t(
                                "src.lib_path.f277.have_old_access_keys"
                            ),
                        ),
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(core.MethodsEnum.AWS_IAM_HAS_OLD_ACCESS_KEYS),
                    aws_response=user,  # type: ignore
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    has_old_ssh_public_keys,
    have_old_creds_enabled,
    have_old_access_keys,
)
