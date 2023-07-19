from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
    Iterable,
)
from dataloaders import (
    get_new_context,
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
    Root,
    RootUnreliableIndicators,
)
import pytest
from roots.domain import (
    get_root_id_by_nickname,
)
from roots.utils import (
    get_last_cloning_successful,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

# Constants

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["nickname", "group_roots", "only_git_roots"],
    [
        [
            "universe",
            [
                GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:45:55+00:00"
                        ),
                        reason="root OK",
                        status=GitCloningStatus.OK,
                        commit="5b5c92105b5c92105b5c92105b5c92105b5c9210",
                        commit_date=datetime.fromisoformat(
                            "2022-02-15T18:45:06.493253+00:00"
                        ),
                    ),
                    created_by="jdoe@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="unittesting",
                    id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    organization_name="okada",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        includes_health_check=True,
                        modified_by="jdoe@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="universe",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                        credential_id=None,
                        gitignore=["bower_components/*", "node_modules/*"],
                        other=None,
                        reason=None,
                        use_vpn=False,
                    ),
                    type=RootType.GIT,
                    unreliable_indicators=RootUnreliableIndicators(
                        unreliable_code_languages=[],
                        unreliable_last_status_update=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                    ),
                ),
                GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus.UNKNOWN,
                        commit="cdd48a681aa96082b3095dc06fb1b15ec4b5ea7b",
                        commit_date=datetime.fromisoformat(
                            "2022-02-15T18:45:06.493253+00:00"
                        ),
                    ),
                    created_by="jdoe@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:39:56+00:00"
                    ),
                    group_name="unittesting",
                    id="765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                    organization_name="okada",
                    state=GitRootState(
                        branch="develop",
                        environment="QA",
                        includes_health_check=False,
                        modified_by="jdoe@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:39:56+00:00"
                        ),
                        nickname="integrates_1",
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/integrates",
                        credential_id=None,
                        gitignore=[],
                        other=None,
                        reason=None,
                        use_vpn=False,
                    ),
                    type=RootType.GIT,
                    unreliable_indicators=RootUnreliableIndicators(
                        unreliable_code_languages=[],
                        unreliable_last_status_update=datetime.fromisoformat(
                            "2020-11-19T13:39:56+00:00"
                        ),
                    ),
                ),
            ],
            True,
        ],
    ],
)
async def test_get_root_id_by_nickname(
    nickname: str,
    group_roots: Iterable[Root],
    only_git_roots: bool,
) -> None:
    root_id = get_root_id_by_nickname(
        nickname, tuple(group_roots), only_git_roots=only_git_roots
    )
    assert root_id == "4039d098-ffc5-4984-8ed3-eb17bca98e19"


@pytest.mark.parametrize(
    ["root_id"],
    [
        ["4039d098-ffc5-4984-8ed3-eb17bca98e19"],
    ],
)
@patch(
    MODULE_AT_TEST + "roots_utils.historic_cloning_grouped",
    new_callable=AsyncMock,
)
async def test_get_last_cloning_successful(
    mock_historic_cloning_grouped: AsyncMock,
    root_id: str,
    mocked_data_for_module: Callable,
) -> None:
    # Set up mock's result using mocked_data_for_module fixture
    mock_historic_cloning_grouped.return_value = mocked_data_for_module(
        mock_path="roots_utils.historic_cloning_grouped",
        mock_args=[root_id],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    item = await get_last_cloning_successful(loaders, root_id)
    assert item
    assert item.status == GitCloningStatus.OK
