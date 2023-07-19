from collections.abc import (
    Callable,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.types import (
    GitRootCloning,
)
import pytest
from typing import (
    Any,
)

MOCKED_DATA: dict[str, dict[str, Any]] = {
    "roots.domain.roots_utils.historic_cloning_grouped": {
        '["4039d098-ffc5-4984-8ed3-eb17bca98e19"]': (
            (
                GitRootCloning(
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    reason="root OK",
                    status=GitCloningStatus.OK,
                    commit="767eb97ba0a02a935541d5b5ed04bfe12f2baf8c",
                    commit_date=datetime.fromisoformat(
                        "2022-02-15T19:10:53.129220+00:00"
                    ),
                ),
            ),
            (
                GitRootCloning(
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:38:00+00:00"
                    ),
                    reason="root FAILED",
                    status=GitCloningStatus.FAILED,
                    commit="767eb97ba0a02a935541d5b5ed04bfe12f2baf8c",
                    commit_date=datetime.fromisoformat(
                        "2022-02-15T19:10:53.129220+00:00"
                    ),
                ),
            ),
            (
                GitRootCloning(
                    modified_date=datetime.fromisoformat(
                        "2020-11-19T13:39:10+00:00"
                    ),
                    reason="root OK",
                    status=GitCloningStatus.OK,
                    commit="767eb97ba0a02a935541d5b5ed04bfe12f2baf8c",
                    commit_date=datetime.fromisoformat(
                        "2022-02-15T19:10:53.129220+00:00"
                    ),
                ),
            ),
        )
    }
}


@pytest.fixture
def mocked_data_for_module(
    *,
    resolve_mock_data: Callable,
) -> Any:
    def _mocked_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCKED_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mocked_data_for_module
