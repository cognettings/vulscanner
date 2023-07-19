# pylint: disable=too-many-arguments
from . import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_secret")
@pytest.mark.parametrize(
    ["email", "key", "value", "group_name", "root_id", "description"],
    [
        [
            "admin@fluidattacks.com",
            "key test",
            "value test",
            "unittesting",
            "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            "description test",
        ],
    ],
)
async def test_add_secret(
    populate: bool,
    email: str,
    key: str,
    value: str,
    group_name: str,
    root_id: str,
    description: str,
) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        key=key,
        value=value,
        group_name=group_name,
        root_id=root_id,
        description=description,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addSecret"]
    assert result["data"]["addSecret"]["success"]

    loaders = get_new_context()
    root_secrets = await loaders.root_secrets.load(root_id)

    new_secret = next(
        (secret for secret in root_secrets if secret.key == key), None
    )
    assert new_secret is not None
    assert new_secret.description == description
    assert new_secret.key == key
    assert new_secret.value == value


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_secret")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@fluidattacks.com"],
    ],
)
async def test_add_secret_fail(
    populate: bool,
    email: str,
) -> None:
    assert populate

    key: str = "key test"
    value: str = "value test"
    group_name: str = "unittesting"
    root_id: str = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    description: str = "description test"

    result: dict[str, Any] = await get_result(
        user=email,
        key=key,
        value=value,
        group_name=group_name,
        root_id=root_id,
        description=description,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
