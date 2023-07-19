from __future__ import (
    annotations,
)

from collections.abc import (
    Callable,
)
from http_headers import (
    as_string,
    content_encoding,
    content_security_policy,
    date,
    referrer_policy,
    set_cookie,
    strict_transport_security,
    upgrade_insecure_requests,
    www_authenticate,
    x_cache,
    x_content_type_options,
)
from http_headers.types import (
    ContentSecurityPolicyHeader,
    Header,
    SetCookieHeader,
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
from multidict import (
    MultiDict,
)
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


class HeaderCheckCtx(NamedTuple):
    url_ctx: URLContext
    headers_parsed: MultiDict[str, Header]  # type: ignore


class Location(NamedTuple):
    description: str
    identifier: str


class Locations(NamedTuple):
    locations: list[Location]

    def append(
        self,
        desc: str,
        desc_kwargs: dict[str, LocalesEnum | str] | None = None,
        identifier: str = "",
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_http.analyze_headers.{desc}",
                    **(desc_kwargs or {}),
                ),
                identifier=identifier,
            )
        )


def _create_vulns(
    locations: Locations,
    header: Header | None,
    ctx: HeaderCheckCtx,
    method: MethodsEnum,
) -> Vulnerabilities:
    return tuple(
        build_inputs_vuln(
            method=method,
            stream="home,response,headers",
            what=ctx.url_ctx.original_url,
            where=location.description,
            metadata=build_metadata(
                method=method,
                description=(
                    f"{location.description} {t(key='words.in')} "
                    f"{ctx.url_ctx.original_url}"
                ),
                snippet=as_string.snippet(
                    url=ctx.url_ctx.original_url,
                    header=header.name if header else None,
                    value=location.identifier,
                    headers=ctx.url_ctx.headers_raw,
                ),
                http_properties=HTTPProperties(
                    has_redirect=ctx.url_ctx.has_redirect,
                    original_url=ctx.url_ctx.original_url,
                ),
            ),
        )
        for location in locations.locations
    )


def _content_security_policy_wild_uri(
    locations: Locations,
    value: str,
    directive: str = "default-src",
) -> None:
    for uri in ("data:", "http:", "https:", "://*"):
        if uri == value:
            locations.append(
                desc="content_security_policy.wild_uri",
                desc_kwargs={
                    "directive": directive,
                    "uri": uri,
                },
            )


def _content_security_policy_block_all_mixed_content(
    locations: Locations,
    header: Header,
) -> None:
    if (
        isinstance(header, ContentSecurityPolicyHeader)
        and "block-all-mixed-content" in header.directives
    ):
        locations.append("content_security_policy.mixed_content_deprecated")


def _content_security_policy_frame_acestors(
    locations: Locations,
    header: Header,
) -> None:
    if isinstance(header, ContentSecurityPolicyHeader):
        if "frame-ancestors" in header.directives:
            values = header.directives.get("frame-ancestors", [])
            for value in values:
                _content_security_policy_wild_uri(locations, value)
        else:
            locations.append("content_security_policy.missing_frame_ancestors")


def _content_security_policy_object_src(
    locations: Locations,
    header: Header,
) -> None:
    if isinstance(header, ContentSecurityPolicyHeader) and (
        "object-src" not in header.directives
        and "default-src" not in header.directives
    ):
        locations.append("content_security_policy.missing_object_src")


def _content_security_policy_script_src(
    locations: Locations,
    header: Header,
) -> None:
    if not isinstance(header, ContentSecurityPolicyHeader):
        return

    if not any(
        directive in header.directives
        for directive in ["default-src", "script-src"]
    ):
        locations.append("content_security_policy.missing_script_src")
        return

    directive = (
        "script-src" if "script-src" in header.directives else "default-src"
    )
    values = header.directives.get(directive, [])
    for value in values:
        if value == "'unsafe-inline'":
            locations.append("content_security_policy.script-src.unsafeinline")

        _content_security_policy_wild_uri(locations, value, directive)

        for arg in (
            "*.amazonaws.com",
            "*.cloudflare.com",
            "*.cloudfront.net",
            "*.doubleclick.net",
            "*.google.com",
            "*.googleapis.com",
            "*.googlesyndication.com",
            "*.newrelic.com",
            "*.s3.amazonaws.com",
            "*.yandex.ru",
            "ajax.googleapis.com",
            "mc.yandex.ru",
            "vk.com",
            "www.google.com",
        ):
            if arg in value:
                locations.append(
                    desc="content_security_policy.script-src.jsonp",
                    desc_kwargs=dict(host=arg),
                )


def _content_security_policy(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    locations = Locations(locations=[])
    header: Header | None = None

    if header := ctx.headers_parsed.get("ContentSecurityPolicyHeader"):
        _content_security_policy_block_all_mixed_content(locations, header)
        _content_security_policy_frame_acestors(locations, header)
        _content_security_policy_object_src(locations, header)
        _content_security_policy_script_src(locations, header)
    else:
        locations.append("content_security_policy.missing")

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.CONTENT_SECURITY_POLICY,
    )


def _upgrade_insecure_requests(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    locations = Locations(locations=[])
    head: Header | None = None

    if not ctx.headers_parsed.get("UpgradeInsecureRequestsHeader") and (
        not (head := ctx.headers_parsed.get("ContentSecurityPolicyHeader"))
        or "upgrade-insecure-requests" not in head.directives
    ):
        locations.append("upgrade_insecure_requests.missing")

    return _create_vulns(
        locations=locations,
        header=head,
        ctx=ctx,
        method=MethodsEnum.UPGRADE_INSEC_REQ,
    )


def _date(ctx: HeaderCheckCtx) -> Vulnerabilities:
    locations = Locations(locations=[])
    header: Header | None = None

    if (
        (header := ctx.headers_parsed.get("DateHeader"))
        # X-Cache means content is served by a CDN, which may cache
        # a previous server response time
        and ctx.headers_parsed.get("XCacheHeader") is None
    ):
        # Exception: WF(Cannot factorize function)
        if ctx.url_ctx.timestamp_ntp:  # NOSONAR
            minutes: float = (
                abs(ctx.url_ctx.timestamp_ntp - header.date.timestamp()) / 60.0
            )

            if minutes > 1:
                locations.append(
                    desc="date.un_synced",
                    desc_kwargs=dict(
                        minutes=str(int(minutes)),
                        minutes_plural="" if minutes == 1 else "s",
                    ),
                )

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.DATE,
    )


def _location(ctx: HeaderCheckCtx) -> Vulnerabilities:
    locations = Locations(locations=[])
    header: Header | None = None

    if response := ctx.url_ctx.custom_f023:
        # Exception: WF(Cannot factorize function)
        if "fluidattacks.com" in response.headers.get(  # NOSONAR
            "location", ""
        ):
            locations.append("location.injection")

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.LOCATION,
    )


def _referrer_policy(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    if not ctx.url_ctx.is_html:
        return ()
    locations = Locations(locations=[])
    header: Header | None = None

    if header := ctx.headers_parsed.get("ReferrerPolicyHeader"):
        for value in header.values:
            # Some header values may be out of the spec or experimental
            # We won't take them into account as some browsers won't
            # support them. The spec says that browsers should read the next
            # value in the comma separated list
            if value in {
                "no-referrer",
                "no-referrer-when-downgrade",
                "origin",
                "origin-when-cross-origin",
                "same-origin",
                "strict-origin",
                "strict-origin-when-cross-origin",
                "unsafe-url",
            }:
                if value not in {
                    "no-referrer",
                    "same-origin",
                    "strict-origin",
                    "strict-origin-when-cross-origin",
                }:
                    locations.append(
                        "referrer_policy.weak",
                        desc_kwargs={"header_value": value},
                        identifier=value,
                    )
                break
        else:
            locations.append("referrer_policy.weak")

    else:
        locations.append("referrer_policy.missing")

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.REFERRER_POLICY,
    )


def _is_sensitive_cookie(cookie_name: str) -> bool:
    sensitive_names = ("session",)
    return any(smell in cookie_name for smell in sensitive_names)


def _set_cookie_httponly(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    locations = Locations(locations=[])

    headers: list[Header] = ctx.headers_parsed.getall(
        key="SetCookieHeader", default=[]
    )

    for header in headers:
        if (
            isinstance(header, SetCookieHeader)
            and _is_sensitive_cookie(header.cookie_name)
            and not header.httponly
        ):
            locations.append(
                desc="set_cookie_httponly.missing_httponly",
                desc_kwargs={"cookie_name": header.cookie_name},
                identifier=header.raw_content,
            )

    return _create_vulns(
        locations=locations,
        header=None if not headers else headers[0],
        ctx=ctx,
        method=MethodsEnum.SET_COOKIE_HTTPONLY,
    )


def _set_cookie_samesite(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    locations = Locations(locations=[])

    headers: list[Header] = ctx.headers_parsed.getall(
        key="SetCookieHeader", default=[]
    )

    for header in headers:
        if (
            isinstance(header, SetCookieHeader)
            and _is_sensitive_cookie(header.cookie_name)
            and header.samesite.lower() != "strict"
        ):
            locations.append(
                desc="set_cookie_samesite.bad_samesite",
                desc_kwargs={"cookie_name": header.cookie_name},
                identifier=header.raw_content,
            )

    return _create_vulns(
        locations=locations,
        header=None if not headers else headers[0],
        ctx=ctx,
        method=MethodsEnum.SET_COOKIE_SAMESITE,
    )


def _set_cookie_secure(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    locations = Locations(locations=[])

    headers: list[Header] = ctx.headers_parsed.getall(
        key="SetCookieHeader", default=[]
    )

    for header in headers:
        if (
            isinstance(header, SetCookieHeader)
            and _is_sensitive_cookie(header.cookie_name)
            and not header.secure
        ):
            locations.append(
                desc="set_cookie_secure.missing_secure",
                desc_kwargs={"cookie_name": header.cookie_name},
                identifier=header.raw_content,
            )

    return _create_vulns(
        locations=locations,
        header=None if not headers else headers[0],
        ctx=ctx,
        method=MethodsEnum.SET_COOKIE_SECURE,
    )


def _strict_transport_security(
    ctx: HeaderCheckCtx,
) -> Vulnerabilities:
    locations = Locations(locations=[])
    header: Header | None = None

    if val := ctx.headers_parsed.get("StrictTransportSecurityHeader"):
        if val.max_age < 31536000:
            locations.append("strict_transport_security.short_max_age")
    else:
        locations.append("strict_transport_security.missing")

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.STRICT_TRANSPORT_SECURITY,
    )


def _www_authenticate(ctx: HeaderCheckCtx) -> Vulnerabilities:
    # You can only see plain-text credentials over http. Avoid FP.
    if not ctx.url_ctx.url.startswith("http://"):  # NOSONAR
        return ()

    locations = Locations(locations=[])
    header: Header | None = None

    if val := ctx.headers_parsed.get("WWWAuthenticate"):
        # Exception: WF(Cannot factorize function)
        if val.type == "basic":  # NOSONAR
            locations.append("www_authenticate.basic")

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.WWW_AUTHENTICATE,
    )


def _x_content_type_options(ctx: HeaderCheckCtx) -> Vulnerabilities:
    locations = Locations(locations=[])
    header: Header | None = None

    if val := ctx.headers_parsed.get("XContentTypeOptionsHeader"):
        if val.value != "nosniff":
            locations.append("x_content_type_options.insecure")
    else:
        locations.append("x_content_type_options.missing")

    return _create_vulns(
        locations=locations,
        header=header,
        ctx=ctx,
        method=MethodsEnum.X_CONTENT_TYPE_OPTIONS,
    )


def get_check_ctx(url: URLContext) -> HeaderCheckCtx:
    headers_parsed: MultiDict[str, Header] = MultiDict(  # type: ignore
        [
            (type(header_parsed).__name__, header_parsed)
            for header_raw_name, header_raw_value in reversed(
                tuple(url.headers_raw.items())
            )
            for line in [f"{header_raw_name}: {header_raw_value}"]
            for header_parsed in [
                content_encoding.parse(line),
                content_security_policy.parse(line),
                date.parse(line),
                referrer_policy.parse(line),
                set_cookie.parse(line),
                strict_transport_security.parse(line),
                upgrade_insecure_requests.parse(line),
                www_authenticate.parse(line),
                x_cache.parse(line),
                x_content_type_options.parse(line),
            ]
            if header_parsed is not None
        ]
    )

    return HeaderCheckCtx(
        url_ctx=url,
        headers_parsed=headers_parsed,
    )


CHECKS: dict[
    FindingEnum,
    list[Callable[[HeaderCheckCtx], Vulnerabilities]],
] = {
    FindingEnum.F015: [_www_authenticate],
    FindingEnum.F023: [_location],
    FindingEnum.F043: [
        _content_security_policy,
        _upgrade_insecure_requests,
    ],
    FindingEnum.F064: [_date],
    FindingEnum.F071: [_referrer_policy],
    FindingEnum.F128: [_set_cookie_httponly],
    FindingEnum.F129: [_set_cookie_samesite],
    FindingEnum.F130: [_set_cookie_secure],
    FindingEnum.F131: [_strict_transport_security],
    FindingEnum.F132: [_x_content_type_options],
}
