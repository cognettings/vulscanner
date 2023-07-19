from aioextensions import (
    collect,
    CPU_CORES,
)
from collections.abc import (
    Callable,
)
from contextlib import (
    suppress,
)
import ctx
from lib.ssl import (
    analyze_protocol,
)
from lib.ssl.suites import (
    SSLVersionId,
)
from lib.ssl.types import (
    SSLContext,
    SSLServerResponse,
)
from model import (
    core,
)
from state.ephemeral import (
    EphemeralStore,
)
from urllib3 import (
    exceptions,
)
from urllib3.util.url import (
    parse_url,
)
from utils.function import (
    shield,
)
from utils.logs import (
    log,
)

CHECKS: tuple[
    dict[
        core.FindingEnum,
        list[Callable[[SSLContext], core.Vulnerabilities]],
    ],
    ...,
] = (analyze_protocol.CHECKS,)

BLACKLISTED_DOMAINS = {
    "amazon-dss.com",
    "amazonaws.com",
    "s3.amazonaws.com",
    "amazonaws.com.cn",
    "amazonaws.org",
    "amazonses.com",
    "amazonwebservices.com",
    "aws.a2z.com",
    "aws.amazon.com",
    "aws.dev",
    "awsstatic.com",
    "elasticbeanstalk.com",
    "azure-api.net",
    "cloudapp.net",
    "cloudapp.azure.com",
    "azurewebsites.net",
    "googleapis.com",
}


@shield(on_error_return=[])
async def analyze_one(
    *,
    index: int,
    ssl_ctx: SSLContext,
    stores: dict[core.FindingEnum, EphemeralStore],
    count: int,
) -> None:
    await log("info", "Analyzing ssl %s of %s: %s", index, count, ssl_ctx)

    for checks in CHECKS:
        for finding, check_list in checks.items():
            if finding in ctx.SKIMS_CONFIG.checks:
                for check in check_list:
                    for vulnerability in check(ssl_ctx):
                        stores[vulnerability.finding].store(vulnerability)


def _get_ssl_targets(urls: set[str]) -> set[tuple[str, int, str]]:
    targets: set[tuple[str, int, str]] = set()
    default_port = 443
    for url in urls:
        with suppress(ValueError, exceptions.HTTPError):
            parsed_url = parse_url(url)
            if not parsed_url.host or parsed_url.host in BLACKLISTED_DOMAINS:
                continue

            if parsed_url.port is None:
                targets.add((parsed_url.host, default_port, url))
            else:
                targets.add((parsed_url.host, parsed_url.port, url))

    return targets


def _get_ssl_context(
    host: str,
    port: int,
    url: str | None,
) -> SSLContext:
    responses: list[SSLServerResponse] = []
    for v_id in SSLVersionId:
        with suppress(Exception):
            if v_id != SSLVersionId.sslv3_0 and (
                tls_response := analyze_protocol.tls_connect(
                    host=host,
                    port=port,
                    v_id=v_id,
                )
            ):
                responses = [*responses, tls_response]

    return SSLContext(
        host=host,
        port=port,
        original_url=url,
        tls_responses=tuple(responses),
    )


async def get_ssl_contexts() -> set[SSLContext]:
    ssl_contexts: set[SSLContext] = set()

    if ctx.SKIMS_CONFIG.dast and ctx.SKIMS_CONFIG.dast.ssl_checks:
        for host, port, url in _get_ssl_targets(
            set(ctx.SKIMS_CONFIG.dast.urls)
        ):
            ssl_contexts.add(_get_ssl_context(host, port, url))

    return ssl_contexts


async def analyze(
    *,
    stores: dict[core.FindingEnum, EphemeralStore],
) -> None:
    if not any(
        finding in ctx.SKIMS_CONFIG.checks
        for checks in CHECKS
        for finding in checks
    ):
        return

    unique_ssl_contexts: set[SSLContext] = await get_ssl_contexts()
    count: int = len(unique_ssl_contexts)

    await collect(
        (
            analyze_one(
                index=index,
                ssl_ctx=ssl_ctx,
                stores=stores,
                count=count,
            )
            for index, ssl_ctx in enumerate(unique_ssl_contexts, start=1)
        ),
        workers=CPU_CORES,
    )
