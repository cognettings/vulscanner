from app import (
    app,
)
from app.middleware import (
    CustomRequestMiddleware,
)
from app.views import (
    auth,
)
from context import (
    FI_STARLETTE_SESSION_KEY,
)
from httpx import (
    AsyncClient,
)
import pytest
from settings import (
    DEBUG,
)
from settings.session import (
    SESSION_COOKIE_SAME_SITE,
)
from starlette.applications import (
    Starlette,
)
from starlette.middleware import (
    Middleware,
)
from starlette.middleware.sessions import (
    SessionMiddleware,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
)
from starlette.routing import (
    Route,
)


async def authz_test(request: Request) -> HTMLResponse:
    user = {
        "iss": "https://accounts.google.com",
        "azp": "335718398321-f7bgci0778rfjt5bdrub4t9tco27j45g",
        "aud": "335718398321-f7bgci0778rfjt5bdrub4t9tco27j45g",
        "sub": "115087346644871393931",
        "hd": "fluidattacks.com",
        "email": "test@fluidattacks.com",
        "email_verified": True,
        "at_hash": "gzHUIo3TNILYi11GsmOi2w",
        "nonce": "nm8nDP2yOD6YevTONDLD",
        "name": "Test Test",
        "picture": "https://lh3.googleusercontent.com/a/",
        "given_name": "Test",
        "family_name": "Test",
        "locale": "en",
        "iat": 1681847316,
        "exp": 1681850916,
    }
    response = RedirectResponse(url="/home")
    await auth.handle_user(request, response, user)  # type: ignore
    return response  # type: ignore


APP = Starlette(
    debug=DEBUG,
    routes=[
        Route("/authz_google", auth.authz_google),
        Route("/authz_test", authz_test),
        Route("/dglogin", auth.do_google_login),
    ],
    middleware=[
        Middleware(
            SessionMiddleware,
            secret_key=FI_STARLETTE_SESSION_KEY,
            same_site=SESSION_COOKIE_SAME_SITE,
            https_only=True,
        ),
        Middleware(CustomRequestMiddleware),
    ],
    exception_handlers=app.exception_handlers,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("redirect_cookies")
async def test_app() -> None:
    async with AsyncClient(
        app=APP, base_url="https://localhost:8001/"
    ) as client:
        response_login = await client.get(
            "/dglogin",
        )
        assert response_login.status_code == 302

        response_test = await client.get(
            "/authz_test",
        )
        assert response_test.status_code == 307
        assert response_test.cookies["session"]
        assert response_test.cookies["integrates_session"]
        assert (
            "samesite=strict"
            not in response_test.headers["set-cookie"].lower()
        )
