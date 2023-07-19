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


async def rds_has_not_deletion_protection(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )
    db_instances = response.get("DBInstances", []) if response else []
    method = core.MethodsEnum.AWS_RDS_HAS_NOT_DELETION_PROTECTION
    vulns: core.Vulnerabilities = ()
    if db_instances:
        for instance in db_instances:
            locations: list[Location] = []
            if not instance.get("DeletionProtection", False):
                instance_arn = instance["DBInstanceArn"]
                locations = [
                    Location(
                        access_patterns=("/DeletionProtection",),
                        arn=(f"{instance_arn}"),
                        values=(instance.get("DeletionProtection"),),
                        description=t(
                            "f256.rds_has_not_termination_protection"
                        ),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=instance,
                ),
            )
    return vulns


async def rds_has_not_automated_backups(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="rds", function="describe_db_instances"
    )
    db_instances = response.get("DBInstances", []) if response else []
    method = core.MethodsEnum.AWS_RDS_HAS_NOT_AUTOMATED_BACKUPS
    vulns: core.Vulnerabilities = ()
    if db_instances:
        for instance in db_instances:
            locations: list[Location] = []
            if instance.get("BackupRetentionPeriod") == 0:
                instance_arn = instance["DBInstanceArn"]
                locations = [
                    Location(
                        access_patterns=("/BackupRetentionPeriod",),
                        arn=(f"{instance_arn}"),
                        values=(instance.get("BackupRetentionPeriod"),),
                        description=t("f256.rds_has_not_automated_backups"),
                    )
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=instance,
                ),
            )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (
    rds_has_not_deletion_protection,
    rds_has_not_automated_backups,
)
