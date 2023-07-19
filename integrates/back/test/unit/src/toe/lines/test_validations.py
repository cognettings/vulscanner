from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from custom_exceptions import (
    InvalidLinesOfCode,
    InvalidModifiedDate,
    InvalidSortsRiskLevel,
    InvalidSortsRiskLevelDate,
    InvalidSortsSuggestions,
)
from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.toe_lines.types import (
    SortsSuggestion,
)
import pytest
from toe.lines.validations import (
    validate_loc,
    validate_loc_deco,
    validate_modified_date,
    validate_modified_date_deco,
    validate_sort_risk_level_deco,
    validate_sort_suggestions,
    validate_sorts_risk_level_date,
    validate_sorts_risk_level_date_deco,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_modified_date() -> None:
    modified_date = datetime_utils.get_now() - timedelta(days=1)
    modified_date_fail = datetime_utils.get_now() + timedelta(days=1)
    validate_modified_date(modified_date)
    with pytest.raises(InvalidModifiedDate):
        validate_modified_date(modified_date_fail)


def test_validate_modified_date_deco() -> None:
    @validate_modified_date_deco("modified_date")
    def decorated_func(modified_date: str) -> str:
        return modified_date

    modified_date = datetime_utils.get_now() - timedelta(days=1)
    modified_date_fail = datetime_utils.get_now() + timedelta(days=1)
    decorated_func(modified_date=modified_date)
    with pytest.raises(InvalidModifiedDate):
        decorated_func(modified_date=modified_date_fail)


def test_validate_loc() -> None:
    validate_loc(loc=4)
    with pytest.raises(InvalidLinesOfCode):
        validate_loc(loc=-4)


def test_validate_loc_deco() -> None:
    @validate_loc_deco(loc_field="loc")
    def decorated_func(loc: int) -> int:
        return loc

    decorated_func(loc=4)
    with pytest.raises(InvalidLinesOfCode):
        decorated_func(loc=-4)


def test_validate_sorts_risk_level_date() -> None:
    modified_date = datetime.now() - timedelta(days=1)
    modified_date_fail = datetime.now() + timedelta(days=1)
    validate_sorts_risk_level_date(modified_date)
    with pytest.raises(InvalidSortsRiskLevelDate):
        validate_sorts_risk_level_date(modified_date_fail)


def test_validate_sorts_risk_level_date_deco() -> None:
    @validate_sorts_risk_level_date_deco("modified_date")
    def decorated_func(modified_date: datetime) -> datetime:
        return modified_date

    modified_date = datetime.now() - timedelta(days=1)
    modified_date_fail = datetime.now() + timedelta(days=1)
    decorated_func(modified_date=modified_date)
    with pytest.raises(InvalidSortsRiskLevelDate):
        decorated_func(modified_date=modified_date_fail)


@pytest.mark.parametrize(
    ["suggestions"],
    [
        [
            [
                SortsSuggestion(
                    "366. Inappropriate coding practices - Transparency "
                    "Conflict",
                    50,
                ),
            ]
        ],
    ],
)
@patch(MODULE_AT_TEST + "is_valid_finding_titles", new_callable=AsyncMock)
async def test_validate_sort_suggestions(
    mock_is_valid_finding_titles: AsyncMock,
    suggestions: list[SortsSuggestion],
    mock_data_for_module: Callable,
) -> None:
    # Set up mock's result using mock_data_for_module fixture
    mock_is_valid_finding_titles.return_value = mock_data_for_module(
        mock_path="is_valid_finding_titles",
        mock_args=[suggestions],
        module_at_test=MODULE_AT_TEST,
    )
    loaders = get_new_context()
    await validate_sort_suggestions(loaders, suggestions)
    assert mock_is_valid_finding_titles.called is True


async def test_valid_suggestions() -> None:
    loaders = get_new_context()

    with pytest.raises(InvalidSortsSuggestions):
        await validate_sort_suggestions(
            loaders,
            [
                SortsSuggestion(
                    "060. Insecure service configuration - Host verification",
                    150,
                ),
            ],
        )
    with pytest.raises(InvalidSortsSuggestions):
        await validate_sort_suggestions(
            loaders,
            [
                SortsSuggestion(
                    "060. Insecure service configuration - Host verification",
                    50,
                ),
                SortsSuggestion(
                    "060. Insecure service configuration - Host verification",
                    60,
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 70
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 10
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 10
                ),
                SortsSuggestion(
                    "428. Inappropriate coding practices - invalid file", 10
                ),
            ],
        )


def test_validate_sort_risk_level_deco() -> None:
    @validate_sort_risk_level_deco(value_field="value")
    def decorated_func(value: int) -> int:
        return value

    decorated_func(value=80)
    with pytest.raises(InvalidSortsRiskLevel):
        decorated_func(value=105)
