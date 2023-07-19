from collections.abc import (
    Callable,
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
    RootUnreliableIndicators,
)
import pytest
from typing import (
    Any,
)

MOCK_DATA: dict[str, dict[str, Any]] = {
    "toe.lines.domain.roots_utils.get_root": {
        '["4039d098-ffc5-4984-8ed3-eb17bca98e19", "unittesting"]': GitRoot(
            cloning=GitRootCloning(
                modified_date=datetime.fromisoformat(
                    "2020-11-19T13:37:10+00:00"
                ),
                reason="root OK",
                status=GitCloningStatus.OK,
                commit="5b5c92105b5c92105b5c92105b5c92105b5c9210",
                commit_date=datetime.fromisoformat(
                    "2022-02-15T18:45:06.493253+00:00"
                ),
            ),
            created_by="jdoe@fluidattacks.com",
            created_date=datetime.fromisoformat("2020-11-19T13:37:10+00:00"),
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
        )
    },
    "toe.lines.domain.toe_lines_model.add": {
        '[["user@gmail.com", 1000, "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",'
        ' "2017-08-01 05:00:00+00:00", "2020-08-01 05:00:00+00:00", '
        '"hacker@test.com", 433, "comment test", true, null, null, false, '
        'null, null, 100, 90], "test/new.new", "unittesting", '
        '"4039d098-ffc5-4984-8ed3-eb17bca98e19"]': None,
    },
    "toe.lines.domain.toe_lines_model.remove": {
        '["unittesting", "4039d098-ffc5-4984-8ed3-eb17bca98e19", '
        '"test/new.new"]': None,
    },
    "toe.lines.domain.toe_lines_model.update_state": {
        '[["test/new.new", "unittesting", '
        '"4039d098-ffc5-4984-8ed3-eb17bca98e19", '
        '["2021-08-01 05:00:00+00:00", "hacker2@test.com", 434, true, null, '
        '"comment test 2", "2020-08-01 05:00:00+00:00", false, '
        '"customer2@gmail.com", "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4", '
        '"2020-08-01 05:00:00+00:00", 1111, "hacker2@test.com", '
        '"2022-08-01 05:00:00+00:00", "2019-08-01 05:00:00+00:00", '
        "50, 70, null, null], null], "
        '["2021-09-01 05:00:00+00:00", "hacker2@test.com", 434, null, '
        '"comment test 2", "customer2@gmail.com", null, false, 1111, '
        '"f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c4", '
        '"2020-08-01 05:00:00+00:00", "2019-08-01 05:00:00+00:00", '
        "50, 70, null, null]]": None,
    },
    "toe.lines.validations.is_valid_finding_titles": {
        '[[["366. Inappropriate coding practices - Transparency Conflict", '
        "50]]]": True,
    },
}


@pytest.fixture
def mock_data_for_module(
    *,
    resolve_mock_data: Callable,
) -> Any:
    def _mock_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCK_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mock_data_for_module
