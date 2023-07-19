from collections import (
    defaultdict,
)
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)

HEADERS = {
    "server": "None",
    "Accept-Encoding": "identity",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "WWW-Authenticate": (
        'OAuth realm="Access to FLUIDIntegrates" charset="UTF-8"'
    ),
    "X-Permitted-Cross-Domain-Policies": "master-only",
    "X-Content-Type-Options": "nosniff",
    "X-XSS-Protection": "0",
    "Cache-Control": "must-revalidate, no-cache, no-store",
    "Content-Security-Policy": (
        "script-src "
        "'self' "
        "'unsafe-inline' "
        "localhost:* "
        "cdn.announcekit.app "
        "bam-cell.nr-data.net "
        "bam.nr-data.net "
        "unpkg.com/react@17/ "
        "unpkg.com/react-dom@17/ "
        "unpkg.com/graphiql/ "
        "https://unpkg.com/graphiql@3.0.0/ "
        "https://unpkg.com/@graphiql/plugin-explorer@0.1.21/ "
        "unpkg.com/@graphiql/plugin-explorer/ "
        "cdn.jsdelivr.net/npm/ "
        "d2yyd1h5u9mauk.cloudfront.net "
        "cdnjs.cloudflare.com/ajax/libs/d3/ "
        "cdnjs.cloudflare.com/ajax/libs/c3/ "
        "https://cdn.logrocket.io "
        "https://cdn.lr-ingest.io "
        "https://cdn.lr-in.com "
        "https://cdn.lr-in-prod.com "
        "https://cdn.lr-ingest.com "
        "js-agent.newrelic.com "
        "fluid-enumerates-05dca28.s3.eu-central-1.amazonaws.com/ "
        "*.front.development.fluidattacks.com "
        "*.front.production.fluidattacks.com "
        "*.cookiebot.com "
        "*.zdassets.com "
        "*.mxpnl.com "
        "*.pingdom.net "
        "*.cloudflareinsights.com "
        "https://js.stripe.com; "
        "frame-ancestors "
        "'self'; "
        "object-src "
        "'none'; "
        "upgrade-insecure-requests;"
        "worker-src "
        "'self' "
        "blob:;"
    ),
    "Permissions-Policy": (
        "geolocation=(self), "
        "midi=(self), "
        "push=(self), "
        "sync-xhr=(self), "
        "microphone=(self), "
        "camera=(self), "
        "magnetometer=(self), "
        "gyroscope=(self), "
        "speaker=(self), "
        "vibrate=(self), "
        "fullscreen=(self), "
        "payment=(self) "
    ),
}


# pylint: disable=too-few-public-methods
class CustomRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request.state.store = defaultdict(lambda: None)
        response = await call_next(request)
        response.headers.update(HEADERS)

        return response
