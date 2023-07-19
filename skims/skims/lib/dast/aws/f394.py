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


async def cloudtrail_files_not_validated(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="cloudtrail", function="describe_trails"
    )
    method = core.MethodsEnum.AWS_CLOUDTRAIL_FILES_NOT_VALIDATED
    trails = response.get("trailList", []) if response else []
    vulns: core.Vulnerabilities = ()
    if trails:
        for trail in trails:
            locations: list[Location] = []
            trail_arn = trail["TrailARN"]
            if not trail["LogFileValidationEnabled"]:
                locations = [
                    *locations,
                    Location(
                        arn=(trail_arn),
                        description=t(
                            "src.lib_path.f394.cfn_log_files_not_validated"
                        ),
                        values=(trail["LogFileValidationEnabled"],),
                        access_patterns=("/LogFileValidationEnabled",),
                    ),
                ]
            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=trail,
                ),
            )

    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (cloudtrail_files_not_validated,)
