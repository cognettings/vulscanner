from collections.abc import (
    Callable,
    Iterable,
)
from datetime import (
    datetime,
    timedelta,
)
from flask import (
    Flask,
    request,
    url_for,
)
from flask.wrappers import (
    Response,
)
from functools import (
    partial,
)
import os
import time
import urllib.parse

APP = Flask(__name__)
ROOT = os.path.dirname(__file__)

# Constants
HEADER_DATE_FMT: str = "%a, %d %b %Y %H:%M:%S GMT"


def add_rule(
    finding: str,
    index: int,
    handler: Callable[[], Response],
) -> None:
    rule: str = f"/{finding}_{index}"
    endpoint: str = f"{finding}_{index}"
    APP.add_url_rule(rule, endpoint, handler)


@APP.route("/")
def home() -> Response:
    # Return a small sitemap with the available URL and methods in the server
    urls: list[str] = []

    for rule in APP.url_map.iter_rules():
        url = request.host_url[:-1] + urllib.parse.unquote(
            url_for(
                rule.endpoint,
                **{arg: f"[{arg}]" for arg in rule.arguments},
            )
        )
        urls.append(
            f"<a href={url}>{url}</a> "
            + ", ".join(rule.methods)  # type: ignore
        )

    content = f'<html><body>{"<br />".join(sorted(urls))}</body></html>'

    return Response(content, content_type="text/html")


def _add_headers(
    finding: str,
    header: str,
    header_values: Iterable[str],
    status: int = 200,
) -> None:
    for index, value in enumerate(header_values):
        add_rule(
            finding,
            index,
            partial(Response, headers={header: value}, status=status),
        )


def add_f015_dast_basic() -> None:
    _add_headers(
        finding="headers_f015",
        header="WWW-Authenticate",
        header_values=[
            "",
            "Basic",
            "Basic realm=host.com",
            'Basic realm=host.com, charset="UTF-8"',
            'Bearer realm=host.com, charset="UTF-8"',
        ],
        status=401,
    )


def _add_f023_0() -> Response:
    # Perform a ugly injection
    if request.headers.get("host"):
        return Response(headers={"Location": request.host_url})
    return Response()


def _add_f023_1() -> Response:
    # Redirects to other "safe" url
    if request.headers.get("host"):
        return Response(headers={"Location": "http://localhost"})
    return Response()


def add_f023() -> None:
    for index, rule in enumerate([_add_f023_0, _add_f023_1]):
        add_rule(
            finding="headers_f023",
            index=index,
            handler=rule,
        )


def add_cookies_unsafe() -> None:
    response: Response = Response()
    response.set_cookie(
        key="session", value="vulnhttponly", samesite="strict", secure=True
    )
    response.set_cookie(
        key="session",
        value="vulnsamesite",
        httponly=True,
        samesite="Lax",
        secure=True,
    )
    response.set_cookie(
        key="session",
        value="vulnsecure",
        httponly=True,
        samesite="strict",
        secure=False,
    )

    add_rule("headers_cookies_unsafe", 0, partial(lambda x: x, response))


def add_cookies_safe() -> None:
    response: Response = Response()
    response.set_cookie(
        key="session",
        value="test",
        httponly=True,
        samesite="strict",
        secure=True,
    )
    response.set_cookie(key="google_analytics", value="test")
    response.set_cookie(key="anything", value="test")

    add_rule("headers_cookies_safe", 0, partial(lambda x: x, response))


def add_unsafe_headers() -> None:
    gmt = time.gmtime()
    gmt_str = time.strftime(HEADER_DATE_FMT, gmt)
    date = datetime.strptime(gmt_str, HEADER_DATE_FMT) - timedelta(hours=1)
    safe_csp = (
        "frame-src 'self' 'unsafe-inline' 'unsafe-eval';"
        + "script-src http: data: *.domain.com;"
        + "block-all-mixed-content;"
    )
    headers = {
        "Content-Security-Policy": safe_csp,
        "X-Frame-Options": "deny",
        "Referrer-Policy": "no-referrer-when-downgrade",
        "Date": date.strftime(HEADER_DATE_FMT),
    }
    content = "<html><body><h1>Unsafe Headers</h1></body></html>"
    response = Response(
        content, content_type="text/html", headers=headers, status=200
    )
    add_rule(
        "headers_unsafe",
        0,
        partial(lambda x: x, response),
    )


def add_safe_headers() -> None:
    safe_csp = (
        "frame-src 'self';"
        + "script-src 'self' 'sha256-/VMQIr9hp56zmea0sU1b7cNYQX0vlTIj1CFg=';"
        + "frame-ancestors: 'none'; object-src: 'none';"
        + "upgrade-insecure-requests=1;"
    )
    headers = {
        "Content-Security-Policy": safe_csp,
        "Strict-Transport-Security": "max-age=31536000",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }
    content = "<html><body><h1>Safe Headers</h1></body></html>"
    response = Response(
        content, content_type="text/html", headers=headers, status=200
    )
    add_rule(
        "headers_safe",
        0,
        partial(lambda x: x, response),
    )


def _add_contents(finding: str, paths: Iterable[str]) -> None:
    for index, path in enumerate(paths):
        with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
            add_rule(
                finding,
                index,
                partial(Response, handle.read()),
            )


def add_content_f036() -> None:
    _add_contents(
        finding="content_f036",
        paths=[
            "templates/f036_0.html",
        ],
    )


def add_content_f086() -> None:
    _add_contents(
        finding="content_f086",
        paths=[
            "templates/f086_0.html",
        ],
    )


def start() -> None:
    APP.run()


# Test for Findings F036, F086 (CONTENT)
add_content_f036()
add_content_f086()

# Tests for Findings 015, 023, 043, 064, 071, 128, 129, 130, 131, 132 (HEADERS)
add_f015_dast_basic()
add_f023()
add_cookies_unsafe()
add_cookies_safe()
add_safe_headers()
add_unsafe_headers()
