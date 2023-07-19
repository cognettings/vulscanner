# pylint: disable=import-error
from . import (
    get_me_access_token,
    get_me_data,
    get_result,
)
from back.test.functional.src.invalidate_access_token import (
    get_result as invalidate_token,
)
from datetime import (
    datetime,
    timedelta,
)
import pytest
import uuid


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_access_token")
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
        ["customer_manager@fluidattacks.com"],
        ["reviewer@gmail.com"],
        ["service_forces@gmail.com"],
    ],
)
async def test_add_access_token(populate: bool, email: str) -> None:
    assert populate
    expiration_time = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time = int(expiration_time.timestamp())
    result = await get_result(
        user=email, expiration_time=ts_expiration_time, name="FirstToken"
    )
    assert "errors" not in result
    assert result["data"]["addAccessToken"]["success"]

    session_jwt = result["data"]["addAccessToken"]["sessionJwt"]
    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert me_token["data"]["me"]["accessTokens"][-1]["lastUse"] is None

    me_data = await get_me_data(user=email, session_jwt=session_jwt)
    assert "errors" not in me_data
    assert len(me_data["data"]["me"]["permissions"]) > 0

    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert me_token["data"]["me"]["accessTokens"][-1]["lastUse"] is not None

    invalidate = await invalidate_token(user=email, token_id=str(uuid.uuid4()))
    assert "errors" in invalidate
    assert (
        invalidate["errors"][0]["message"]
        == "Exception - Access denied or token not found"
    )

    invalidate = await invalidate_token(
        user=email, token_id=me_token["data"]["me"]["accessTokens"][-1]["id"]
    )
    assert "errors" not in invalidate
    assert invalidate["data"]["invalidateAccessToken"]["success"]

    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert me_token["data"]["me"]["accessTokens"] == []


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_access_token")
async def test_add_access_token_invalid_time(populate: bool) -> None:
    assert populate
    expiration_time = datetime.utcnow() + timedelta(weeks=30)
    ts_expiration_time = int(expiration_time.timestamp())
    result = await get_result(
        user="admin@gmail.com",
        expiration_time=ts_expiration_time,
        name="Valid",
    )

    assert "errors" in result
    assert (
        result["errors"][0]["message"] == "Exception - Invalid Expiration Time"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_access_token")
async def test_add_access_token_second(populate: bool) -> None:
    assert populate
    email = "hacker@gmail.com"
    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert len(me_token["data"]["me"]["accessTokens"]) == 0

    expiration_time = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time = int(expiration_time.timestamp())
    result = await get_result(
        user=email, expiration_time=ts_expiration_time, name="FirstToken"
    )
    assert "errors" not in result
    assert result["data"]["addAccessToken"]["success"]

    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert len(me_token["data"]["me"]["accessTokens"]) == 1

    expiration_time = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time = int(expiration_time.timestamp())
    result = await get_result(
        user=email, expiration_time=ts_expiration_time, name="SecondToken"
    )
    assert "errors" not in result
    assert result["data"]["addAccessToken"]["success"]

    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert len(me_token["data"]["me"]["accessTokens"]) == 2


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_access_token")
async def test_add_access_token_invalid_name(populate: bool) -> None:
    assert populate
    email = "admin@gmail.com"
    expiration_time = datetime.utcnow() + timedelta(weeks=30)
    ts_expiration_time = int(expiration_time.timestamp())
    result = await get_result(
        user=email, expiration_time=ts_expiration_time, name="= Invalid"
    )

    assert "errors" in result
    assert result["errors"][0]["message"] == "Exception - Invalid characters"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_access_token")
async def test_add_access_token_third(populate: bool) -> None:
    assert populate
    email = "hacker@gmail.com"
    me_token = await get_me_access_token(user=email)
    assert "errors" not in me_token
    assert len(me_token["data"]["me"]["accessTokens"]) == 2

    expiration_time = datetime.utcnow() + timedelta(weeks=8)
    ts_expiration_time = int(expiration_time.timestamp())
    result = await get_result(
        user=email, expiration_time=ts_expiration_time, name="ThirdToken"
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == (
        "Exception - Could not add token, maximum number"
        " of tokens at the same time is 2"
    )
