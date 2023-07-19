import ast
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


async def bucket_policy_has_server_side_encryption_disable(
    credentials: AwsCredentials,
) -> core.Vulnerabilities:
    method = core.MethodsEnum.AWS_BUCKET_POLICY_ENCRYPTION_DISABLE
    response: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="s3",
        function="list_buckets",
    )
    buckets = response.get("Buckets", []) if response else []
    vulns: core.Vulnerabilities = ()
    for bucket in buckets:
        locations: list[Location] = []
        bucket_policy_string: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="s3",
            function="get_bucket_policy",
            parameters={
                "Bucket": str(bucket["Name"]),
            },
        )
        if bucket_policy_string:
            policy = ast.literal_eval(str(bucket_policy_string["Policy"]))
            bucket_statements = policy["Statement"]

            for index, stm in enumerate(bucket_statements):
                if (
                    (conditions := stm.get("Condition", None))
                    and conditions.get("Null", None)
                    and conditions["Null"].get(
                        "s3:x-amz-server-side-encryption", None
                    )
                    and conditions["Null"]["s3:x-amz-server-side-encryption"]
                    != "true"
                ):
                    condition = stm["Condition"]["Null"][
                        "s3:x-amz-server-side-encryption"
                    ]
                    locations = [
                        *locations,
                        Location(
                            access_patterns=(
                                (
                                    f"/Statement/{index}/Condition/Null"
                                    "/s3:x-amz-server-side-encryption"
                                ),
                            ),
                            arn=(f"arn:aws:s3:::{bucket['Name']}"),
                            values=(f"{condition}",),
                            description=t(
                                "f099.s3_has_server_side_encryption_disabled"
                            ),
                        ),
                    ]

            vulns = (
                *vulns,
                *build_vulnerabilities(
                    locations=locations,
                    method=(method),
                    aws_response=policy,
                ),
            )
    return vulns


CHECKS: tuple[
    Callable[[AwsCredentials], Coroutine[Any, Any, tuple[Vulnerability, ...]]],
    ...,
] = (bucket_policy_has_server_side_encryption_disable,)
