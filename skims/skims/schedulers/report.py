import boto3
from contextlib import (
    suppress,
)
import ctx
from dynamodb.types import (
    Item,
)
import json
from model.core import (
    TechniqueEnum,
    Vulnerability,
)
from utils.repositories import (
    get_repo_head_hash,
)


def set_advisories(vulnerability: Vulnerability) -> Item | None:
    return (
        {
            "cve": vulnerability.skims_metadata.cve,
            "vulnerable_version": (
                vulnerability.skims_metadata.vulnerable_version
            ),
            "package": vulnerability.skims_metadata.package,
        }
        if vulnerability.skims_metadata.cve
        else None
    )


def send_vulnerability_to_sqs(vulnerability: Vulnerability) -> None:
    if not (execution_id := ctx.SKIMS_CONFIG.execution_id):
        return
    namespace = ctx.SKIMS_CONFIG.namespace
    working_dir = ctx.SKIMS_CONFIG.working_dir

    client = boto3.client("sqs")
    group_name = execution_id.split("_", maxsplit=1)[0]
    vuln_json = {
        "lines": [
            *(
                [
                    {
                        "commit_hash": get_repo_head_hash(working_dir),
                        "line": str(vulnerability.where),
                        "path": vulnerability.what,
                        "repo_nickname": namespace,
                        "state": "open",
                        "skims_method": (
                            vulnerability.skims_metadata.source_method
                        ),
                        "skims_technique": (
                            vulnerability.skims_metadata.technique.value
                        ),
                        "developer": (
                            vulnerability.skims_metadata.developer.value
                        ),
                        "source": "MACHINE",
                        "hash": vulnerability.digest_future,
                        "cwe_ids": vulnerability.skims_metadata.cwe_ids,
                        "cvss_v3": vulnerability.skims_metadata.cvss,
                        "advisories": set_advisories(vulnerability),
                    }
                ]
                if vulnerability.skims_metadata.technique
                in (
                    TechniqueEnum.BASIC_SAST,
                    TechniqueEnum.ADVANCE_SAST,
                    TechniqueEnum.APK,
                    TechniqueEnum.SCA,
                )
                else []
            )
        ],
        "inputs": [
            *(
                [
                    {
                        "field": str(vulnerability.where),  # noqa
                        "repo_nickname": namespace,
                        "state": "open",
                        "stream": [vulnerability.stream],
                        "url": vulnerability.what,
                        "skims_method": (
                            vulnerability.skims_metadata.source_method
                        ),
                        "skims_technique": (
                            vulnerability.skims_metadata.technique.value
                        ),
                        "technique": (
                            vulnerability.skims_metadata.technique.value
                        ),
                        "developer": (
                            vulnerability.skims_metadata.developer.value
                        ),
                        "source": "MACHINE",
                        "hash": vulnerability.digest_future,
                        "cwe_ids": vulnerability.skims_metadata.cwe_ids,
                        "cvss_v3": vulnerability.skims_metadata.cvss,
                    }
                ]
                if vulnerability.skims_metadata.technique == TechniqueEnum.DAST
                else []
            )
        ],
    }
    with suppress(Exception):
        client.send_message(
            QueueUrl=(
                "https://sqs.us-east-1.amazonaws.com/205810638802/"
                "integrates_report_soon"
            ),
            MessageBody=json.dumps(
                {
                    "id": (
                        f"{group_name}_{namespace}"
                        f"_{vulnerability.digest_future}"
                    ),
                    "task": "report_soon",
                    "args": [
                        group_name,
                        namespace,
                        vulnerability.finding.value.title.split(".")[2],
                        vulnerability.finding.value.auto_approve,
                        vuln_json,
                    ],
                }
            ),
        )
