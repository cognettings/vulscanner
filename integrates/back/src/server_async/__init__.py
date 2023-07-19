from async_sqs_consumer.queue import (
    Queue,
)
from async_sqs_consumer.worker import (
    Worker,
)
from batch_dispatch.clone_roots import (
    clone_git_root_simple_args,
)
from batch_dispatch.rebase import (
    queue_rebase_async,
    rebase_root_simple_args,
)
from batch_dispatch.refresh_toe_inputs import (
    refresh_toe_inputs_simple_args,
)
from batch_dispatch.refresh_toe_lines import (
    refresh_toe_lines_simple_args,
)
from custom_utils.bugsnag import (
    start_scheduler_session,
)
from dynamodb.types import (
    Item,
)
from server_async.enqueue import (
    queue_refresh_toe_lines_async,
)
from server_async.report_machine import (
    process_execution,
)
from server_async.report_machine.soon import (
    process_vulnerabilities,
)

worker = Worker(
    max_workers=10,
    queues={
        "report": Queue(
            url=(
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/integrates_report"
            ),
            max_queue_parallel_messages=20,
            visibility_timeout=240,
            priority=1,
        ),
        "report_soon": Queue(
            url=(
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/integrates_report_soon"
            ),
            max_queue_parallel_messages=20,
            visibility_timeout=240,
            priority=1,
        ),
        "clone": Queue(
            url=(
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/integrates_clone"
            ),
            max_queue_parallel_messages=20,
            visibility_timeout=1000,
            priority=2,
        ),
        "refresh": Queue(
            url=(
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/integrates_refresh"
            ),
            max_queue_parallel_messages=20,
            visibility_timeout=1200,
            priority=3,
        ),
        "rebase": Queue(
            url=(
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/integrates_rebase"
            ),
            max_queue_parallel_messages=20,
            visibility_timeout=1200,
            priority=4,
        ),
    },
)


@worker.on_event("startup")  # type: ignore
async def start_bugsnag() -> None:
    start_scheduler_session()


@worker.task("clone", queue_name="clone")
async def clone(
    group_name: str, git_root_id: str, refresh_next_next: bool = False
) -> None:
    await clone_git_root_simple_args(group_name, git_root_id)
    if refresh_next_next:
        await queue_refresh_toe_lines_async(group_name, git_root_id)


@worker.task("refresh_toe_lines", queue_name="refresh")
async def refresh_toe_lines(
    group_name: str, git_root_id: str, rebase_next: bool = False
) -> None:
    await refresh_toe_lines_simple_args(group_name, git_root_id)
    if rebase_next:
        await queue_rebase_async(group_name, git_root_id)


@worker.task("refresh_toe_inputs", queue_name="refresh")
async def refresh_toe_inputs(group_name: str, url_root_id: str) -> None:
    await refresh_toe_inputs_simple_args(group_name, url_root_id)


@worker.task("rebase", queue_name="rebase")
async def rebase(group_name: str, git_root_id: str) -> None:
    await rebase_root_simple_args(group_name, git_root_id)


@worker.task("report", queue_name="report")
async def report(execution_id: str) -> None:
    await process_execution(execution_id)


@worker.task("report_soon", queue_name="report_soon")
async def report_soon(
    group_name: str,
    git_root_nickname: str,
    finding_code: str,
    auto_approve: bool,
    vulnerability_file: dict[str, list[dict[str, Item]]],
) -> None:
    await process_vulnerabilities(
        group_name,
        git_root_nickname,
        finding_code,
        auto_approve,
        vulnerability_file,
    )


if __name__ == "__main__":
    worker.start()
