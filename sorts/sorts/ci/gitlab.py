from collections.abc import (
    Iterator,
)
from config.typing import (
    Config,
)
from contextlib import (
    contextmanager,
)
from gitlab import (
    Gitlab,
)
from gitlab.v4.objects import (
    Project,
    ProjectMergeRequest,
)
import os


@contextmanager
def client(*, token_gitlab: str) -> Iterator[Gitlab]:
    yield Gitlab(private_token=token_gitlab)


def set_reviewers(*, token_gitlab: str, config: Config) -> None:
    with client(token_gitlab=token_gitlab) as gl_client:
        project_id: str = os.environ["CI_PROJECT_ID"]
        mr_iid: str = os.environ["CI_MERGE_REQUEST_IID"]
        project: Project = gl_client.projects.get(project_id)
        merge_request: ProjectMergeRequest = project.mergerequests.get(mr_iid)
        merge_request.approval_rules.create(
            {
                "approvals_required": config.ci.required_approvals,
                "name": "sorts",
                "user_ids": config.ci.reviewers,
            }
        )
        merge_request.save()
