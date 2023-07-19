from __future__ import (
    annotations,
)

from collections.abc import (
    Callable,
)
from contextlib import (
    suppress,
)
from dns import (
    exception,
    resolver,
)
from lib.http.types import (
    URLContext,
)
from model.core import (
    FindingEnum,
    HTTPProperties,
    LocalesEnum,
    MethodsEnum,
    Vulnerabilities,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
import textwrap
from typing import (
    NamedTuple,
)
from vulnerabilities import (
    build_inputs_vuln,
    build_metadata,
)
from zone import (
    t,
)


class DNSCheckCtx(NamedTuple):
    url_ctx: URLContext


class Location(NamedTuple):
    description: str
    snippet: str


class Locations(NamedTuple):
    locations: list[Location]

    def append(
        self,
        desc: str,
        snippet: str,
        **desc_kwargs: LocalesEnum,
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_http.analyze_dns.{desc}",
                    **desc_kwargs,
                ),
                snippet=snippet,
            )
        )


def _add_dns_location(
    ctx: DNSCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="missing_dmarc",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 2.2.1 of "dnspython"
                >>> from dns import resolver

                >>> # This object will help us analyze the domain
                >>> resolution = resolver.Resolver()

                >>> # Check TXT records in the domain
                >>> resolution.resolve(
                >>>   "_dmarc." + {repr(ctx.url_ctx.get_base_domain())}, "TXT",
                >>>   lifetime=2.0
                >>> )

                []  # Empty list means no dmarc record exist in the domain
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=15, wrap=True),
        ).content,
    )


def _build_dns_vulnerabilities(
    ctx: DNSCheckCtx,
    locations: Locations,
    method: MethodsEnum,
) -> Vulnerabilities:
    return tuple(
        build_inputs_vuln(
            method=method,
            stream="home,response,dns",
            what=ctx.url_ctx.original_url,
            where=location.description,
            metadata=build_metadata(
                method=method,
                description=(
                    f"{location.description} {t(key='words.in')} "
                    f"{ctx.url_ctx.original_url}"
                ),
                snippet=location.snippet,
                http_properties=HTTPProperties(
                    has_redirect=ctx.url_ctx.has_redirect,
                    original_url=ctx.url_ctx.original_url,
                ),
            ),
        )
        for location in locations.locations
    )


def _query_dns(domain: str, timeout: float = 2.0) -> list:
    resolution = resolver.Resolver()
    record_type = "TXT"
    resolution.resolve(domain, record_type, lifetime=timeout)
    try:
        resource_records = list(
            map(
                lambda r: r.strings,
                resolution.resolve(
                    "_dmarc." + domain, record_type, lifetime=timeout
                ),
            )
        )
        _resource_record = [
            resource_record[0][:0].join(resource_record)
            for resource_record in resource_records
            if resource_record
        ]
        records = [r.decode() for r in _resource_record]
    except resolver.NXDOMAIN:
        records = []

    return records


def _check_dns_records(ctx: DNSCheckCtx) -> Vulnerabilities:
    locations = Locations(locations=[])
    domain = ctx.url_ctx.get_base_domain()
    with suppress(exception.DNSException):
        records = _query_dns(domain)
        if len(records) == 0:
            _add_dns_location(ctx, locations)

    return _build_dns_vulnerabilities(
        locations=locations,
        ctx=ctx,
        method=MethodsEnum.CHECK_DNS_RECORDS,
    )


def get_check_ctx(url: URLContext) -> DNSCheckCtx:
    return DNSCheckCtx(
        url_ctx=url,
    )


CHECKS: dict[
    FindingEnum,
    list[Callable[[DNSCheckCtx], Vulnerabilities]],
] = {
    FindingEnum.F182: [_check_dns_records],
}
