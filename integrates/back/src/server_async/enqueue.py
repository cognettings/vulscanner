from botocore.exceptions import (
    ClientError,
)
from contextlib import (
    suppress,
)
import json
from sqs.resources import (
    get_sqs_resource,
)


async def queue_refresh_toe_lines_async(
    group_name: str, git_root_id: str
) -> None:
    with suppress(ClientError):
        await (await get_sqs_resource()).send_message(
            QueueUrl=(
                "https://sqs.us-east-1.amazonaws.com/205810638802/"
                "integrates_refresh"
            ),
            MessageBody=json.dumps(
                {
                    "id": f"{group_name}_{git_root_id}",
                    "task": "refresh_toe_lines",
                    "args": [
                        group_name,
                        git_root_id,
                        True,
                    ],
                }
            ),
        )


async def queue_refresh_toe_inputs_async(
    group_name: str, git_root_id: str
) -> None:
    with suppress(ClientError):
        await (await get_sqs_resource()).send_message(
            QueueUrl=(
                "https://sqs.us-east-1.amazonaws.com/205810638802/"
                "integrates_refresh"
            ),
            MessageBody=json.dumps(
                {
                    "id": f"{group_name}_{git_root_id}",
                    "task": "refresh_toe_lines",
                    "args": [
                        group_name,
                        git_root_id,
                        True,
                    ],
                }
            ),
        )
