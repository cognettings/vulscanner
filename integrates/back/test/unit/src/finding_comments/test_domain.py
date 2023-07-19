from back.test.unit.src.utils import (
    get_module_at_test,
)
from collections.abc import (
    Callable,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.finding_comments.enums import (
    CommentType,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from finding_comments import (
    domain as comments_domain,
)
import pytest
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["group_name", "finding_id", "user_email"],
    [
        ["unittesting", "436992569", "unittest@fluidattacks.com"],
    ],
)
@patch(
    MODULE_AT_TEST + "authz.get_group_level_enforcer", new_callable=AsyncMock
)
@patch(MODULE_AT_TEST + "_fill_vuln_info", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_vulnerabilities",
    new_callable=AsyncMock,
)
@patch(
    MODULE_AT_TEST + "Dataloaders.finding_historic_verification",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_unformatted_comments", new_callable=AsyncMock)
async def test_list_comments(
    # pylint: disable=too-many-arguments, too-many-locals
    mock_get_unformatted_comments: AsyncMock,
    mock_dataloaders_finding_historic_verification: AsyncMock,
    mock_dataloaders_finding_vulnerabilities: AsyncMock,
    mock__fill_vuln_info: AsyncMock,
    mock_get_group_level_enforcer: AsyncMock,
    group_name: str,
    finding_id: str,
    user_email: str,
    mocked_data_for_module: Any,
    side_effect_get_group_level_enforcer: Callable[[str, str], bool],
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_unformatted_comments,
            "get_unformatted_comments",
            [finding_id],
        ),
        (
            mock_dataloaders_finding_historic_verification.load,
            "Dataloaders.finding_historic_verification",
            [finding_id],
        ),
        (
            mock_dataloaders_finding_vulnerabilities.load,
            "Dataloaders.finding_vulnerabilities",
            [finding_id],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for mock_item in mocks_setup_list:
        mock, path, arguments = mock_item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    mock__fill_vuln_info.side_effect = mocked_data_for_module(
        mock_path="_fill_vuln_info",
        mock_args=[finding_id],
        module_at_test=MODULE_AT_TEST,
    )
    # Set up mock's side_effect using side_effect_get_group_level_enforcer
    # fixture
    mock_get_group_level_enforcer.side_effect = (
        side_effect_get_group_level_enforcer
    )
    loaders: Dataloaders = get_new_context()
    test_data = await comments_domain.get_comments(
        loaders=loaders,
        group_name=group_name,
        finding_id=finding_id,
        user_email=user_email,
    )
    expected_output = [
        FindingComment(
            finding_id="436992569",
            id="1558048727111",
            parent_id="0",
            comment_type=CommentType.VERIFICATION,
            creation_date=datetime.fromisoformat("2020-02-21T15:41:04+00:00"),
            content="Regarding vulnerabilities: \n  - 192.168.100.101\n\nthis "
            "is a commenting test of a verifying request verification in "
            "vulns",
            email="integrateshacker@fluidattacks.com",
            full_name="hacker Integrates",
        ),
        FindingComment(
            finding_id="436992569",
            id="1558048727000",
            parent_id="0",
            comment_type=CommentType.VERIFICATION,
            creation_date=datetime.fromisoformat("2020-02-19T15:41:04+00:00"),
            content="Regarding vulnerabilities: \n  - 192.168.100.101\n  - "
            "192.168.100.112\n\nThis is a commenting test of a request "
            "verification in vulns",
            email="integratesuser@gmail.com",
            full_name="user Integrates",
        ),
    ]
    assert isinstance(test_data, tuple)
    assert isinstance(test_data[0], FindingComment)
    assert test_data[0] is not None
    assert sorted(test_data) == sorted(expected_output)
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)
    assert mock__fill_vuln_info.call_count == 3
    assert mock_get_group_level_enforcer.called is True
