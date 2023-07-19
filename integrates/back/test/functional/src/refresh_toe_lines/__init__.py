# pylint: disable=import-error
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from back.test.functional.src.utils import (
    get_graphql_result,
)
from batch_dispatch.refresh_toe_lines import (
    refresh_toe_lines_simple_args,
)
from dataloaders import (
    get_new_context,
)
import git_self
import glob
import os
import shutil
from typing import (
    Any,
)


async def get_result(
    *,
    user: str,
    group_name: str,
    monkeypatch: MonkeyPatch,
) -> dict[str, Any]:
    def mocked_pull_repositories(
        tmpdir: str, group_name: str, repo_nickname: str
    ) -> None:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "mocks")
        fusion_path = f"{tmpdir}/groups/{group_name}"
        if repo_nickname:
            shutil.copytree(
                f"{filename}/{repo_nickname}", f"{fusion_path}/{repo_nickname}"
            )
        else:
            shutil.copytree(filename, fusion_path)

        git_mocks = glob.glob(f"{fusion_path}/*/.git_mock")
        for git_mock in git_mocks:
            os.rename(git_mock, git_mock.replace("/.git_mock", "/.git"))

    query: str = f"""
        mutation {{
            refreshToeLines(
                groupName: "{group_name}",
            ) {{
                success
            }}
        }}
    """
    data: dict[str, Any] = {"query": query}
    result = await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
    if result["data"]:
        monkeypatch.setattr(
            git_self,
            "pull_repositories",
            mocked_pull_repositories,
        )
        await refresh_toe_lines_simple_args(
            group_name, "63298a73-9dff-46cf-b42d-9b2f01a56690"
        )
    return result


async def query_get(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            name
            toeLines {{
                edges {{
                    node {{
                        attackedAt
                        attackedBy
                        attackedLines
                        bePresent
                        bePresentUntil
                        comments
                        filename
                        firstAttackAt
                        lastAuthor
                        lastCommit
                        loc
                        modifiedDate
                        seenAt
                        sortsRiskLevel
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
    }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
