from back.test.unit.src.utils import (
    get_module_at_test,
    set_mocks_return_values,
)
from custom_utils.group_comments import (
    format_group_consulting_resolve,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.group_comments.types import (
    GroupComment,
)
from group_comments.domain import (
    get_comments,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["email", "group_name"],
    [
        [
            "integratesmanager@gmail.com",
            "unittesting",
        ],
    ],
)
@patch(MODULE_AT_TEST + "Dataloaders.group_comments", new_callable=AsyncMock)
@patch("authz.enforcer.get_user_level_role", new_callable=AsyncMock)
@patch(
    "authz.enforcer.Dataloaders.stakeholder_groups_access",
    new_callable=AsyncMock,
)
async def test_get_comments(
    mock_authz_enforcer_dataloaders: AsyncMock,
    mock_authz_enforcer_get_user_level_role: AsyncMock,
    mock_dataloaders_group_comments: AsyncMock,
    email: str,
    group_name: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[email]],
        mocked_objects=[mock_authz_enforcer_dataloaders.load],
        module_at_test="authz.enforcer.",
        paths_list=["Dataloaders.stakeholder_groups_access"],
    )
    mock_authz_enforcer_get_user_level_role.return_value = "admin"
    assert set_mocks_return_values(
        mocks_args=[[group_name]],
        mocked_objects=[mock_dataloaders_group_comments.load],
        module_at_test=MODULE_AT_TEST,
        paths_list=["Dataloaders.group_comments"],
    )

    test_data = await get_comments(get_new_context(), group_name, email)

    expected_output = GroupComment(
        group_name="unittesting",
        content="Now we can post comments on groups",
        parent_id="0",
        creation_date=datetime.fromisoformat("2018-12-27T21:30:28+00:00"),
        id="1545946228675",
        full_name="Miguel de Orellana",
        email="unittest@fluidattacks.com",
    )
    expected_output_to_resolve = {
        "content": "Now we can post comments on groups",
        "parent": "0",
        "created": "2018/12/27 16:30:28",
        "id": "1545946228675",
        "fullname": "Fluid Attacks",
        "email": "help@fluidattacks.com",
        "modified": "2018/12/27 16:30:28",
    }
    assert test_data[0] == expected_output

    assert (
        format_group_consulting_resolve(
            group_comment=test_data[0], target_email="nonfluid@test.test"
        )
        == expected_output_to_resolve
    )
    assert mock_authz_enforcer_dataloaders.load.called is True
    assert mock_authz_enforcer_get_user_level_role.called is True
    assert mock_dataloaders_group_comments.load.called is True
