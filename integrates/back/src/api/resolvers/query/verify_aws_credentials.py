from .schema import (
    QUERY,
)
import aioboto3
import botocore
from custom_utils import (
    logs as logs_utils,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
)


async def run_boto3_fun(
    credentials: dict[str, str],
    service: str,
    function: str,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    try:
        session = aioboto3.Session(
            aws_access_key_id=credentials["access_key_id"],
            aws_secret_access_key=credentials["secret_access_key"],
        )
        async with session.client(
            service,
        ) as client:
            return await getattr(client, function)(**(parameters or {}))
    except botocore.exceptions.ClientError as exc:
        logs_utils.cloudwatch_log(
            exc, "Security: Attempted to validate AWS credentials"
        )
        return {}


@QUERY.field("verifyAwsCredentials")
@require_login
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    access_key_id: str,
    secret_access_key: str,
    **_kwargs: None,
) -> bool:
    aws_managed_arn = "arn:aws:iam::aws"
    credentials = {
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
    }

    user_request: dict[str, Any] = await run_boto3_fun(
        credentials,
        service="iam",
        function="get_user",
    )
    if user_request != {}:
        groups_request: dict[str, Any] = await run_boto3_fun(
            credentials,
            service="iam",
            function="list_groups_for_user",
            parameters={"UserName": str(user_request["User"]["UserName"])},
        )

        for group in groups_request["Groups"]:
            group_policies: dict[str, Any] = await run_boto3_fun(
                credentials,
                service="iam",
                function="list_attached_group_policies",
                parameters={"GroupName": str(group["GroupName"])},
            )
            for policy in group_policies["AttachedPolicies"]:
                if str(policy["PolicyName"]) == "ReadOnlyAccess" and str(
                    policy["PolicyArn"]
                ).startswith(aws_managed_arn):
                    return True

    return False
