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


async def bucket_has_object_lock_disabled(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    response: dict[str, Any] = await run_boto3_fun(
        credentials, service="s3", function="list_buckets"
    )
    buckets = response.get("Buckets", []) if response else []
    method = core.MethodsEnum.AWS_S3_BUCKETS_HAS_OBJECT_LOCK_DISABLED
    vulns: core.Vulnerabilities = ()
    if buckets:
        for bucket in buckets:
            locations: list[Location] = []
            bucket_name = bucket["Name"]
            bucket_grants: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="s3",
                function="get_object_lock_configuration",
                parameters={"Bucket": str(bucket_name)},
            )
            conf = bucket_grants.get("ObjectLockConfiguration", {})
            if conf:
                if conf.get("ObjectLockEnabled") != "Enabled":
                    locations = [
                        *[
                            Location(
                                access_patterns=(
                                    "/ObjectLockConfiguration/"
                                    "ObjectLockEnabled",
                                ),
                                arn=(f"arn:aws:s3:::{bucket_name}"),
                                values=(conf.get("ObjectLockEnabled"),),
                                description=t(
                                    "src.lib_path.f101."
                                    "bucket_has_object_lock_disabled"
                                ),
                            )
                        ],
                    ]
                    vulns = (
                        *vulns,
                        *build_vulnerabilities(
                            locations=locations,
                            method=method,
                            aws_response=bucket_grants,
                        ),
                    )
            else:
                locations = [
                    *[
                        Location(
                            access_patterns=(),
                            arn=(f"arn:aws:s3:::{bucket_name}"),
                            values=(),
                            description=t(
                                "src.lib_path.f101."
                                "bucket_has_object_lock_disabled"
                            ),
                        )
                    ],
                ]
                vulns = (
                    *vulns,
                    *build_vulnerabilities(
                        locations=locations,
                        method=method,
                        aws_response=bucket,
                    ),
                )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (bucket_has_object_lock_disabled,)
