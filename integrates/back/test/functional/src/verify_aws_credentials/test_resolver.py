from . import (
    put_mutation,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("verify_aws_credentials")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
    ],
)
async def test_get_report_toe_lines(populate: bool, email: str) -> None:
    assert populate
    result: dict = await put_mutation(
        user=email,
        access_key_id="AKIAIOSFODNN7EXAMPLE",
        secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLE",
    )
    assert not result["data"]["verifyAwsCredentials"]
