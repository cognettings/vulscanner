from . import (
    get_result,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("download_file")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_download_file(populate: bool, email: str) -> None:
    assert populate
    file_name: str = "test.zip"
    result: dict[str, Any] = await get_result(
        user=email,
        group="group1",
        f_name=file_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["downloadFile"]
    assert result["data"]["downloadFile"]["success"]
    assert "url" in result["data"]["downloadFile"]
