from aioextensions import (
    collect,
)
import asyncio
from batch_dispatch.rebase import (
    queue_rebase_async,
)
import boto3
from context import (
    FI_AWS_REGION_NAME,
)
from custom_utils.findings import (
    get_requirements_file,
    get_vulns_file,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
)
from dynamodb.types import (
    Item,
)
from functools import (
    partial,
)
from groups.domain import (
    get_group,
)
import logging
from organizations.utils import (
    get_organization,
)
from server_async.report_machine.finding import (
    filter_same_findings,
)
from server_async.report_machine.vulnerability import (
    process_criteria_vuln,
)
from server_async.utils import (
    decode_sqs_message,
    delete_message,
    get_config,
    get_sarif_log,
)
from signal import (
    SIGINT,
    signal,
    SIGTERM,
)
from typing import (
    Any,
    NamedTuple,
)

logging.getLogger("boto").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("boto3").setLevel(logging.ERROR)

# Constants
LOGGER = logging.getLogger(__name__)


class Context(NamedTuple):
    loaders: Dataloaders
    headers: dict[str, str]


class SignalHandler:  # pylint: disable=too-few-public-methods
    def __init__(self) -> None:
        self.received_signal = False
        signal(SIGINT, self._signal_handler)  # type: ignore
        signal(SIGTERM, self._signal_handler)  # type: ignore

    def _signal_handler(self, _signal: str, _: None) -> None:
        print(f"handling signal {_signal}, exiting gracefully")
        self.received_signal = True


async def process_execution(
    execution_id: str,
    criteria_vulns: Item | None = None,
    criteria_reqs: Item | None = None,
    config_path: str | None = None,
    sarif_path: str | None = None,
) -> bool:
    # pylint: disable=too-many-locals
    criteria_vulns = criteria_vulns or await get_vulns_file()
    criteria_reqs = criteria_reqs or await get_requirements_file()
    loaders: Dataloaders = get_new_context()
    group_name = execution_id.split("_", maxsplit=1)[0]
    group: Group | None = await loaders.group.load(group_name)
    if group and (
        group.state.has_machine is False
        or group.state.managed == GroupManaged.UNDER_REVIEW
    ):
        LOGGER.warning(
            "",
            extra={
                "extra": {
                    "execution_id": execution_id,
                    "group_name": group_name,
                }
            },
        )
        return False
    execution_config = await get_config(execution_id, config_path)
    try:
        git_root = next(
            root
            for root in await loaders.group_roots.load(group_name)
            if isinstance(root, GitRoot)
            and root.state.status == RootStatus.ACTIVE
            and root.state.nickname == execution_config["namespace"]
        )
    except StopIteration:
        LOGGER.warning(
            "Could not find root for the execution",
            extra={
                "extra": {
                    "execution_id": execution_id,
                    "nickname": execution_config["namespace"],
                }
            },
        )
        return False
    results = await get_sarif_log(execution_id, sarif_path)
    if not results:
        LOGGER.warning(
            "Could not find execution result",
            extra={"extra": {"execution_id": execution_id}},
        )
        return False

    rules_id: set[str] = {
        item["id"] for item in results["runs"][0]["tool"]["driver"]["rules"]
    }
    if not rules_id:
        return True
    auto_approve_rules: dict[str, bool] = {
        item["id"]: item.get("properties", {}).get("auto_approve", False)
        for item in results["runs"][0]["tool"]["driver"]["rules"]
    }

    group_findings = await loaders.group_findings.load(group_name)
    rules_finding: list[tuple[str, tuple[Finding, ...]]] = []
    for criteria_vuln_id in rules_id:
        same_type_of_findings: list = []
        for finding in group_findings:
            filter_same_findings(
                criteria_vuln_id, finding, same_type_of_findings
            )
        rules_finding.append((criteria_vuln_id, tuple(same_type_of_findings)))

    organization_name = (
        await get_organization(
            loaders, (await get_group(loaders, group_name)).organization_id
        )
    ).name
    number_of_affected_vulnerabilities = sum(
        result or 0
        for result in await collect(
            [
                process_criteria_vuln(
                    loaders=loaders,
                    group_name=group_name,
                    vulnerability_id=vuln_id,
                    criteria_vulnerability=criteria_vulns[vuln_id],
                    criteria_requirements=criteria_reqs,
                    same_type_of_findings=same_type_of_findings,
                    language=str(execution_config["language"]).lower(),
                    git_root=git_root,
                    sarif_log=results,
                    execution_config=execution_config,
                    organization_name=organization_name,
                    auto_approve=auto_approve_rules[vuln_id],
                )
                for vuln_id, same_type_of_findings in rules_finding
            ]
        )
    )
    if number_of_affected_vulnerabilities > 0:
        await queue_rebase_async(
            group_name,
            git_root.id,
        )

    return True


def _callback_done(
    future: asyncio.Future, *, message: Any, queue: Any
) -> None:
    if future.done():
        if exception := future.exception():
            message_id = decode_sqs_message(message)
            LOGGER.error(
                "An error has occurred consuming a report",
                extra={
                    "extra": {
                        "execution_id": message_id,
                        "exception": str(exception),
                    }
                },
            )
        else:
            delete_message(queue, message)


async def main() -> None:
    criteria_vulns = await get_vulns_file()
    criteria_reqs = await get_requirements_file()
    sqs = boto3.resource("sqs", region_name=FI_AWS_REGION_NAME)
    queue = sqs.get_queue_by_name(QueueName="skims-report-queue")
    signal_handler = SignalHandler()
    while not signal_handler.received_signal:
        while len(asyncio.all_tasks()) > 10:
            await asyncio.sleep(0.3)

        messages = queue.receive_messages(
            MessageAttributeNames=[],
            MaxNumberOfMessages=10,
            VisibilityTimeout=600,
        )
        if not messages:
            messages = queue.receive_messages(
                MessageAttributeNames=[],
                MaxNumberOfMessages=10,
                VisibilityTimeout=600,
                WaitTimeSeconds=20,
            )
            if not messages:
                break

        for message in messages:
            task = asyncio.create_task(
                process_execution(
                    decode_sqs_message(message),
                    criteria_vulns,
                    criteria_reqs,
                )
            )
            task.add_done_callback(
                partial(_callback_done, message=message, queue=queue)
            )
