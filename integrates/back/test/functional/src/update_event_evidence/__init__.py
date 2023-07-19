# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import os
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    event: str,
) -> dict[str, Any]:
    query: str = """
        mutation updateEventEvidence(
            $eventId: String!,
            $evidenceType: EventEvidenceType!,
            $file: Upload!
        ) {
            updateEventEvidence(
                eventId: $eventId
                evidenceType: $evidenceType
                groupName: "group1"
                file: $file
            ) {
                success
            }
        }
    """
    path: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = f"{path}/test-anim.webm"
    with open(filename, "rb") as test_file:
        uploaded_file: UploadFile = UploadFile(
            "orgtest-group1-lkjhgfdas2.webm", test_file, "video/webm"
        )
        variables: dict[str, Any] = {
            "eventId": event,
            "evidenceType": "IMAGE_1",
            "file": uploaded_file,
        }
        data: dict[str, Any] = {"query": query, "variables": variables}
        result: dict[str, Any] = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )
    return result
