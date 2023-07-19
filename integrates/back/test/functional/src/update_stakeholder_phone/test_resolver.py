from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_stakeholder_phone")
@pytest.mark.parametrize(
    ("email", "new_phone", "verification_code"),
    (
        (
            "admin@gmail.com",
            {"callingCountryCode": "1", "nationalNumber": "12345"},
            "12134",
        ),
    ),
)
async def test_update_stakeholder_phone(
    populate: bool,
    email: str,
    new_phone: dict[str, str],
    verification_code: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        new_phone=new_phone,
        verification_code=verification_code,
    )
    assert "errors" not in result
    assert result["data"]["updateStakeholderPhone"]["success"]
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    assert stakeholder
    assert stakeholder.phone
    assert stakeholder.phone.national_number == new_phone["nationalNumber"]
