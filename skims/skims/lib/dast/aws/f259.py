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


async def dynamodb_has_not_deletion_protection(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="dynamodb", function="list_tables"
    )
    table_names = response.get("TableNames", []) if response else []
    method = core.MethodsEnum.AWS_DYNAMODB_NOT_DEL_PROTEC
    vulns: core.Vulnerabilities = ()
    if table_names:
        for table in table_names:
            locations: list[Location] = []
            describe_table: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_table",
                parameters={
                    "TableName": table,
                },
            )
            table_arn = describe_table["Table"]["TableArn"]
            del_protec = describe_table["Table"].get(
                "DeletionProtection", None
            )

            if del_protec is None:
                locations = [
                    Location(
                        access_patterns=("/Table",),
                        arn=(table_arn),
                        values=(describe_table["Table"],),
                        description=t(
                            "src.lib_root.f259."
                            "dynamo_has_not_deletion_protection"
                        ),
                    ),
                ]
            elif del_protec not in {True, "true", "True"}:
                locations = [
                    Location(
                        access_patterns=("/Table/DeletionProtection",),
                        arn=(table_arn),
                        values=(
                            describe_table["Table"]["DeletionProtection"],
                        ),
                        description=t(
                            "src.lib_root.f259."
                            "dynamo_has_not_deletion_protection"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=describe_table,
                ),
            )
    return vulns


async def dynamodb_has_not_point_in_time_recovery(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="dynamodb", function="list_tables"
    )
    table_names = response.get("TableNames", []) if response else []
    method = core.MethodsEnum.AWS_DYNAMODB_HAS_NOT_POINT_IN_TIME_RECOVERY
    vulns: core.Vulnerabilities = ()
    if table_names:
        for table in table_names:
            locations: list[Location] = []

            table_backup: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_continuous_backups",
                parameters={
                    "TableName": table,
                },
            )
            describe_table: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="dynamodb",
                function="describe_table",
                parameters={
                    "TableName": table,
                },
            )
            table_arn = describe_table["Table"]["TableArn"]
            backup_description = table_backup.get(
                "ContinuousBackupsDescription", {}
            )

            if (
                backup_description["PointInTimeRecoveryDescription"][
                    "PointInTimeRecoveryStatus"
                ]
                == "DISABLED"
            ):
                locations = [
                    Location(
                        access_patterns=(
                            (
                                "/ContinuousBackupsDescription/"
                                "PointInTimeRecoveryDescription/"
                                "PointInTimeRecoveryStatus"
                            ),
                        ),
                        arn=(table_arn),
                        values=(
                            backup_description[
                                "PointInTimeRecoveryDescription"
                            ]["PointInTimeRecoveryStatus"],
                        ),
                        description=t(
                            "src.lib_path.f259.has_not_point_in_time_recovery"
                        ),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=table_backup,
                ),
            )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    dynamodb_has_not_deletion_protection,
    dynamodb_has_not_point_in_time_recovery,
)
