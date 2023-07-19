# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesState,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("update_toe_lines_attacked_lines")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="universe",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="asm_1",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/asm_1",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by="admin@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group3",
                    id="86e9b0a8-b6be-4b3f-8006-a9a060f69e81",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        gitignore=["node_modules/*"],
                        includes_health_check=True,
                        modified_by="admin@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="asm_1",
                        other=None,
                        reason=None,
                        status=RootStatus.INACTIVE,
                        url="https://gitlab.com/fluidattacks/asm_1",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
        ],
        "toe_lines": (
            ToeLines(
                filename="test/test#.config",
                group_name="group1",
                root_id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                state=ToeLinesState(
                    attacked_at=None,
                    attacked_by="test@test.com",
                    attacked_lines=23,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=None,
                    has_vulnerabilities=False,
                    last_author="customer1@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    loc=4324,
                    modified_by="test@test.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=0,
                ),
            ),
            ToeLines(
                filename="test2/test.sh",
                group_name="group2",
                root_id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-02-20T05:00:00+00:00"
                    ),
                    attacked_by="test2@test.com",
                    attacked_lines=4,
                    be_present=True,
                    be_present_until=None,
                    comments="comment 2",
                    first_attack_at=datetime.fromisoformat(
                        "2020-02-19T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-15T15:41:04+00:00"
                    ),
                    loc=180,
                    modified_by="test2@test.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2020-02-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=-1,
                ),
            ),
            ToeLines(
                filename="test3/test.config",
                group_name="group3",
                root_id="86e9b0a8-b6be-4b3f-8006-a9a060f69e81",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2020-01-14T15:41:04+00:00"
                    ),
                    attacked_by="test3@test.com",
                    attacked_lines=120,
                    be_present=True,
                    be_present_until=None,
                    comments="",
                    first_attack_at=datetime.fromisoformat(
                        "2020-01-14T15:41:04+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer3@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c3",
                    last_commit_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    loc=243,
                    modified_by="test3@test.com",
                    modified_date=datetime.fromisoformat(
                        "2020-11-16T15:41:04+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2019-01-01T15:41:04+00:00"
                    ),
                    sorts_risk_level=80,
                ),
            ),
        ),
    }

    return await db.populate({**generic_data["db_data"], **data})
