from contextlib import (
    suppress,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.types import (
    Item,
)
from findings.domain.evidence import (
    update_evidence,
)
import random
from server_async.utils import (
    to_png,
)
from starlette.datastructures import (
    UploadFile,
)


async def upload_evidences(
    loaders: Dataloaders,
    finding: Finding,
    machine_vulnerabilities: list[Item],
) -> bool:
    success: bool = True
    evidence_ids = [("evidence_route_5", "evidence_route_5")]
    number_of_samples: int = min(
        len(machine_vulnerabilities), len(evidence_ids)
    )
    result_samples: tuple[Item, ...] = tuple(
        random.sample(machine_vulnerabilities, k=number_of_samples),
    )
    evidence_descriptions = [
        result["message"]["text"] for result in result_samples
    ]
    evidence_streams: tuple[UploadFile, ...] = tuple()
    for result in result_samples:
        evidence_streams = (
            *evidence_streams,
            await to_png(
                string=result["locations"][0]["physicalLocation"]["region"][
                    "snippet"
                ]["text"]
            ),
        )
    for (evidence_id, _), evidence_stream, evidence_description in zip(
        evidence_ids, evidence_streams, evidence_descriptions
    ):
        # Exception may happen
        # due to two reports trying to update the evidence concurrently
        # or trying to upload the same evidence
        with suppress(ConditionalCheckFailedException):
            await update_evidence(
                loaders,
                finding.id,
                evidence_id,
                evidence_stream,
                description=evidence_description,
                is_draft=False,
            )

    loaders.finding.clear(finding.id)
    return success
