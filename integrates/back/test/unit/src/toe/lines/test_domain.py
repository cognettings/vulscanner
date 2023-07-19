from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_lines.types import (
    ToeLines,
    ToeLinesState,
)
from freezegun import (
    freeze_time,
)
import pytest
from toe.lines.domain import (
    add,
    remove,
    update,
)
from toe.lines.types import (
    ToeLinesAttributesToAdd,
    ToeLinesAttributesToUpdate,
)
from typing import (
    Any,
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
    ["group_name", "root_id", "filename", "attributes"],
    [
        [
            "unittesting",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "test/new.new",
            ToeLinesAttributesToAdd(
                attacked_at=datetime.fromisoformat(
                    "2020-08-01T05:00:00+00:00"
                ),
                attacked_by="hacker@test.com",
                attacked_lines=433,
                comments="comment test",
                last_author="user@gmail.com",
                has_vulnerabilities=False,
                loc=1000,
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                last_commit_date=datetime.fromisoformat(
                    "2017-08-01T05:00:00+00:00"
                ),
                sorts_risk_level=100,
                sorts_priority_factor=90,
            ),
        ],
    ],
)
@patch(MODULE_AT_TEST + "toe_lines_model.add", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "roots_utils.get_root", new_callable=AsyncMock)
async def test_add(  # pylint: disable=too-many-arguments
    mock_roots_utils_get_root: AsyncMock,
    mock_toe_lines_model_add: AsyncMock,
    mock_data_for_module: Callable,
    group_name: str,
    root_id: str,
    filename: str,
    attributes: ToeLinesAttributesToAdd,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_roots_utils_get_root,
            "roots_utils.get_root",
            [root_id, group_name],
        ),
        (
            mock_toe_lines_model_add,
            "toe_lines_model.add",
            [attributes, filename, group_name, root_id],
        ),
    ]
    # Set up mocks' results using mock_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mock_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )

    loaders = get_new_context()
    await add(loaders, group_name, root_id, filename, attributes)
    assert mock_roots_utils_get_root.called is True
    assert mock_toe_lines_model_add.called is True


@pytest.mark.parametrize(
    ("current_value", "attributes", "expected_new_state"),
    (
        (
            ToeLines(
                filename="test/new.new",
                group_name="unittesting",
                root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                state=ToeLinesState(
                    attacked_at=datetime.fromisoformat(
                        "2021-08-01T05:00:00+00:00"
                    ),
                    attacked_by="hacker2@test.com",
                    attacked_lines=434,
                    be_present=True,
                    be_present_until=None,
                    comments="comment test 2",
                    first_attack_at=datetime.fromisoformat(
                        "2020-08-01T05:00:00+00:00"
                    ),
                    has_vulnerabilities=False,
                    last_author="customer2@gmail.com",
                    last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
                    last_commit_date=datetime.fromisoformat(
                        "2020-08-01T05:00:00+00:00"
                    ),
                    loc=1111,
                    modified_by="hacker2@test.com",
                    modified_date=datetime.fromisoformat(
                        "2022-08-01T05:00:00+00:00"
                    ),
                    seen_at=datetime.fromisoformat(
                        "2019-08-01T05:00:00+00:00"
                    ),
                    sorts_risk_level=50,
                    sorts_priority_factor=70,
                    sorts_risk_level_date=None,
                    sorts_suggestions=None,
                ),
                seen_first_time_by=None,
            ),
            ToeLinesAttributesToUpdate(
                attacked_at=datetime.fromisoformat(
                    "2021-09-01T05:00:00+00:00"
                ),
                attacked_by="hacker2@test.com",
                attacked_lines=434,
                comments="comment test 2",
                last_author="customer2@gmail.com",
                has_vulnerabilities=False,
                loc=1111,
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
                last_commit_date=datetime.fromisoformat(
                    "2020-08-01T05:00:00+00:00"
                ),
                seen_at=datetime.fromisoformat("2019-08-01T05:00:00+00:00"),
                sorts_risk_level=50,
                sorts_priority_factor=70,
            ),
            ToeLinesState(
                attacked_at=datetime.fromisoformat(
                    "2021-09-01T05:00:00+00:00"
                ),
                attacked_by="hacker2@test.com",
                attacked_lines=434,
                be_present=True,
                be_present_until=None,
                comments="comment test 2",
                first_attack_at=datetime.fromisoformat(
                    "2020-08-01T05:00:00+00:00"
                ),
                has_vulnerabilities=False,
                last_author="customer2@gmail.com",
                last_commit="f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4",
                last_commit_date=datetime.fromisoformat(
                    "2020-08-01T05:00:00+00:00"
                ),
                loc=1111,
                modified_by="hacker2@test.com",
                modified_date=datetime.fromisoformat(
                    "2022-08-01T05:00:00+00:00"
                ),
                seen_at=datetime.fromisoformat("2019-08-01T05:00:00+00:00"),
                sorts_risk_level=50,
                sorts_priority_factor=70,
                sorts_risk_level_date=None,
                sorts_suggestions=None,
            ),
        ),
    ),
)
@patch(MODULE_AT_TEST + "toe_lines_model.update_state", new_callable=AsyncMock)
@freeze_time("2022-08-01T05:00:00+00:00")
async def test_update(
    mock_toe_lines_model_update_state: AsyncMock,
    mock_data_for_module: Callable,
    current_value: ToeLines,
    attributes: ToeLinesAttributesToUpdate,
    expected_new_state: ToeLinesState,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_toe_lines_model_update_state.return_value = mock_data_for_module(
        mock_path="toe_lines_model.update_state",
        mock_args=[current_value, attributes],
        module_at_test=MODULE_AT_TEST,
    )

    await update(current_value, attributes)

    mock_toe_lines_model_update_state.assert_called_with(
        current_value=current_value, new_state=expected_new_state
    )
    assert mock_toe_lines_model_update_state.called is True


@pytest.mark.parametrize(
    ["group_name", "root_id", "filename"],
    [
        [
            "unittesting",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "test/new.new",
        ],
    ],
)
@patch(MODULE_AT_TEST + "toe_lines_model.remove", new_callable=AsyncMock)
async def test_remove(
    mock_toe_lines_model_remove: AsyncMock,
    mock_data_for_module: Callable,
    group_name: str,
    root_id: str,
    filename: str,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_toe_lines_model_remove.return_value = mock_data_for_module(
        mock_path="toe_lines_model.remove",
        mock_args=[group_name, root_id, filename],
        module_at_test=MODULE_AT_TEST,
    )
    await remove(group_name, root_id, filename)
    assert mock_toe_lines_model_remove.called is True
