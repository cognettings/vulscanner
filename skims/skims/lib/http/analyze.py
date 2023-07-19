import bs4
from collections.abc import (
    Callable,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
import ctx
from datetime import (
    datetime,
)
from lib.http import (
    analyze_content,
    analyze_dns,
    analyze_headers,
)
from lib.http.types import (
    URLContext,
)
from model.core import (
    FindingEnum,
    Vulnerabilities,
    Vulnerability,
)
from more_itertools import (
    collapse,
)
from queue import (
    SimpleQueue,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)
from urllib3.util.url import (
    get_host,
)
from urllib.parse import (
    urlparse,
)
from utils.function import (
    shield_blocking,
)
from utils.html import (
    get_alternative_protocol_urls,
    get_sameorigin_urls,
    is_html,
)
from utils.http import (
    create_session,
    request,
)
from utils.logs import (
    log_blocking,
)
from utils.ntp import (
    get_offset,
)

CHECKS: tuple[
    tuple[
        Callable[[URLContext], Any],
        dict[
            FindingEnum,
            list[Callable[[Any], Vulnerabilities]],
        ],
    ],
    ...,
] = (
    (analyze_content.get_check_ctx, analyze_content.CHECKS),
    (analyze_dns.get_check_ctx, analyze_dns.CHECKS),
    (analyze_headers.get_check_ctx, analyze_headers.CHECKS),
)


@shield_blocking(on_error_return=[])
def analyze_one(
    *,
    index: int,
    url: URLContext,
    unique_count: int,
) -> tuple[Vulnerability, ...]:
    log_blocking(
        "info", "Analyzing http %s of %s: %s", index, unique_count, url
    )
    vulns: tuple[Vulnerability, ...] = tuple()

    for get_check_ctx, checks in CHECKS:
        url_ctx = get_check_ctx(url)
        for finding, check_list in checks.items():
            if (
                finding not in ctx.SKIMS_CONFIG.checks
                or (
                    url.response_status >= 400
                    and finding is not FindingEnum.F015
                )
                or (url.response_status != 401 and finding is FindingEnum.F015)
            ):
                continue

            for check in check_list:
                vulns += check(url_ctx)

    return vulns


# @rate_limited(rpm=LIB_HTTP_DEFAULT)
async def get_url(
    url: str,
    *,
    ntp_offset: float | None,
    included_urls: set[str],
) -> URLContext | None:
    # Urls for common attached file extensions should be excluded from analysis
    ignored_ext = (
        "css",
        "js",
        "jpg",
        "jpeg",
        "png",
    )
    if url.endswith(ignored_ext):
        return None

    async with create_session() as session:  # type: ignore
        if response := await request(session, "GET", url):
            redirect_url = str(response.url)
            if redirect_url in included_urls:
                # Url is already included in analysis
                return None

            # If the redirected vuln domain is different than the original url
            # it should not be analyzed
            if get_host(redirect_url)[1] != get_host(url)[1]:
                return None

            content_raw = await response.content.read(1048576)
            content = content_raw.decode("latin-1")
            soup = bs4.BeautifulSoup(content, features="html.parser")

            return URLContext(
                components=urlparse(redirect_url),
                content=content,
                custom_f023=await request(
                    session,
                    "GET",
                    url,
                    headers={
                        "Host": "fluidattacks.com",
                    },
                ),
                has_redirect=redirect_url.rstrip("/") != url.rstrip("/"),
                headers_raw=response.headers,  # type: ignore
                is_html=is_html(content, soup),
                original_url=url,
                soup=soup,
                timestamp_ntp=(
                    datetime.now().timestamp() + ntp_offset
                    if ntp_offset
                    else None
                ),
                url=redirect_url,
                response_status=response.status,
            )

    log_blocking("warning", "Unable to create url context for %s", url)

    return None


async def get_urls() -> set[URLContext]:
    urls_to_analyze: set[URLContext] = set()
    urls_done: set[str] = set()
    urls_pending: SimpleQueue = SimpleQueue()
    ntp_offset: float | None = get_offset()

    if ctx.SKIMS_CONFIG.dast and ctx.SKIMS_CONFIG.dast.http_checks:
        for url in get_alternative_protocol_urls(
            set(ctx.SKIMS_CONFIG.dast.urls)
        ):
            urls_pending.put(url)

    while not urls_pending.empty():
        url = urls_pending.get()

        url_ctx: URLContext | None = await get_url(
            url,
            ntp_offset=ntp_offset,
            included_urls={url.url for url in urls_to_analyze},
        )
        if url_ctx is None:
            continue

        urls_to_analyze.add(url_ctx)
        urls_done.add(url)

        for child_url in get_sameorigin_urls(url_ctx.components, url_ctx.soup):
            if child_url not in urls_done:
                log_blocking("info", "Discovered url: %s", child_url)

    return urls_to_analyze


async def analyze(
    *,
    stores: dict[FindingEnum, EphemeralStore],
) -> None:
    if not any(
        finding in ctx.SKIMS_CONFIG.checks
        for _, checks in CHECKS
        for finding in checks
    ):
        return

    unique_urls: set[URLContext] = await get_urls()
    unique_count: int = len(unique_urls)

    with ThreadPoolExecutor() as executor:
        vulnerabilities: tuple[Vulnerability, ...] = tuple(
            collapse(
                (
                    analyze_one(
                        index=index,
                        url=url,
                        unique_count=unique_count,
                    )
                    for index, url in enumerate(unique_urls, start=1)
                ),
                base_type=Vulnerability,
            )
        )
        executor.map(
            lambda x: stores[  # pylint: disable=unnecessary-lambda
                x.finding
            ].store(x),
            vulnerabilities,
        )
