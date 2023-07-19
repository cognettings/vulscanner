from gitlab import (
    Gitlab,
)
from gitlab.exceptions import (
    GitlabDeleteError,
)
from gitlab.v4.objects import (
    ProjectBranch,
    ProjectMergeRequest,
)
import logging
import os

logging.basicConfig(level=logging.INFO)

# Constants
LOGGER = logging.getLogger(__name__)
PROJECT_ID = os.environ["CI_PROJECT_ID"]
PROTECTED_BRANCHES = set(["trunk", "dmurciaatfluid"])
TOKEN = os.environ["UNIVERSE_API_TOKEN"]
URL = "https://gitlab.com"
SESSION = Gitlab(URL, private_token=TOKEN)
PROJECT = SESSION.projects.get(PROJECT_ID)


def get_all_branches() -> set[str]:
    branches: list[ProjectBranch] = PROJECT.branches.list()
    return set(branch.name for branch in branches)


def get_users_opened_merge_request() -> set[str]:
    opened_merge_request: list[
        ProjectMergeRequest
    ] = PROJECT.mergerequests.list(state="opened", sort="asc")
    opened_mr_id = [
        merge_request.iid for merge_request in opened_merge_request
    ]

    if not opened_mr_id:
        return set()

    return set(
        PROJECT.mergerequests.get(merge_request).author["username"]
        for merge_request in opened_mr_id
    )


def cancel_pipeline(*, pipeline_id: str) -> None:
    pipeline = PROJECT.pipelines.get(pipeline_id)
    response = pipeline.cancel()
    if "message" in response:
        LOGGER.error(
            "Failed to cancel pipeline %s with message: %s",
            pipeline_id,
            response.get("message", "unknown error"),
        )

    LOGGER.info(
        "Pipeline canceled %s -> %s",
        pipeline_id,
        response.get("status", "unknown status"),
    )


def get_user_running_pipelines(*, username: str) -> list[str]:
    pipelines = PROJECT.pipelines.list(
        ref=username, username=username, status="running"
    )
    return [pipeline.id for pipeline in pipelines]


def delete_branch(*, branch: str) -> None:
    user_running_pipelines = get_user_running_pipelines(username=branch)
    if user_running_pipelines:
        for pipeline_id in user_running_pipelines:
            cancel_pipeline(pipeline_id=pipeline_id)

    try:
        PROJECT.branches.delete(branch)
    except GitlabDeleteError:
        LOGGER.info("Branch %s already deleted", branch)


def delete_repository_branches(*, branches: set[str]) -> None:
    if not branches:
        LOGGER.info("Everything is up to date!")
        return

    for branch in branches:
        LOGGER.info("Deleting %s branch!", branch)
        delete_branch(branch=branch)
        LOGGER.info("Branch %s successfully deleted!", branch)


def main():
    all_users_branches = get_all_branches()
    users_opened_mr = get_users_opened_merge_request()
    branches_to_delete = (
        all_users_branches - PROTECTED_BRANCHES - users_opened_mr
    )
    delete_repository_branches(branches=branches_to_delete)


if __name__ == "__main__":
    main()
