# pylint: disable-all
# type: ignore

from pyramid.authentication import (
    AuthTktAuthenticationPolicy,
    AuthTktCookieHelper,
)
from starlette.responses import (
    HTMLResponse,
    PlainTextResponse,
)


async def index(request):
    response = PlainTextResponse("Cookie set!")
    response.set_cookie(
        "my_cookie", "cookie_value", secure=True, httponly=True
    )
    return response


def set_token_in_response(response: HTMLResponse, token: str) -> HTMLResponse:
    response.set_cookie(
        key="JWT_COOKIE_NAME",
        samesite="JWT_COOKIE_SAMESITE",
        value=token,
        secure=False,
        httponly=False,
        max_age="SESSION_COOKIE_AGE",
    )
    return response


def my_bad_view1(request):
    response = request.response
    response.set_cookie(
        "MY_COOKIE", value="MY_COOKIE_VALUE", secure=True, httponly=False
    )


def bad1():
    authtkt = AuthTktCookieHelper(secret="test", httponly=False)
    return authtkt


def bad2():
    authtkt = AuthTktAuthenticationPolicy(secret="test", httponly=False)
    return authtkt
