from . import (
    get_result,
)
from custom_exceptions import (
    ErrorUpdatingGroup,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    GroupFile,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_remove_files(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    file_name: str = "test.zip"
    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.files
    assert len(group.files) == 4
    file_to_remove: GroupFile = next(
        file for file in group.files if file.file_name == file_name
    )
    assert file_to_remove

    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["removeFiles"]
    assert result["data"]["removeFiles"]["success"]

    loaders.group.clear(group_name)
    group_updated = await loaders.group.load(group_name)
    assert group_updated
    assert group_updated.files
    assert len(group_updated.files) == 3
    file_removed: GroupFile | None = next(
        (file for file in group_updated.files if file.file_name == file_name),
        None,
    )
    assert file_removed is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_remove_files_fail_1(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == ErrorUpdatingGroup.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("remove_files")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_remove_files_fail_2(populate: bool, email: str) -> None:
    assert populate
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
