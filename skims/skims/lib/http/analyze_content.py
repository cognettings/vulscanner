from __future__ import (
    annotations,
)

from bs4.element import (
    Tag,
)
from collections.abc import (
    Callable,
    Iterable,
)
import contextlib
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
from typing import (
    NamedTuple,
)
from urllib.parse import (
    urlparse,
)
import viewstate
from vulnerabilities import (
    build_inputs_vuln,
    build_metadata,
)
from zone import (
    t,
)


class ContentCheckCtx(NamedTuple):
    url_ctx: URLContext


class Location(NamedTuple):
    description: str
    column: int
    line: int

    @classmethod
    def from_soup_tag(
        cls: object,
        tag: Tag,
        desc: str,
        desc_kwargs: dict[str, LocalesEnum] | None = None,
    ) -> Location:
        return Location(
            description=t(
                f"lib_http.analyze_content.{desc}",
                **(desc_kwargs or {}),
            ),
            column=tag.sourcepos,
            line=tag.sourceline,
        )


def _build_content_vulnerabilities(
    locations: Iterable[Location],
    ctx: ContentCheckCtx,
    method: MethodsEnum,
) -> Vulnerabilities:
    return tuple(
        build_inputs_vuln(
            method=method,
            stream="home,response,content",
            what=ctx.url_ctx.original_url,
            where=str(location.line),
            metadata=build_metadata(
                method=method,
                description=(
                    f"{location.description} {t(key='words.in')} "
                    f"{ctx.url_ctx.original_url}"
                ),
                snippet=make_snippet(
                    content=ctx.url_ctx.content,
                    viewport=SnippetViewport(
                        column=location.column,
                        line=location.line,
                    ),
                ).content,
                http_properties=HTTPProperties(
                    has_redirect=ctx.url_ctx.has_redirect,
                    original_url=ctx.url_ctx.original_url,
                ),
            ),
        )
        for location in locations
    )


def _sub_resource_integrity(
    ctx: ContentCheckCtx,
) -> Vulnerabilities:
    locations: list[Location] = []

    for script in ctx.url_ctx.soup.find_all("script"):
        if not script.get("integrity") and (src := script.get("src")):
            netloc = urlparse(src).netloc

            for domain in (
                "cloudflareinsights.com",
                "cookiebot.com",
                "newrelic.com",
                "nr-data.net",
            ):
                if netloc.endswith(domain):
                    locations.append(
                        Location.from_soup_tag(
                            desc="sub_resource_integrity.missing_integrity",
                            desc_kwargs=dict(netloc=netloc),
                            tag=script,
                        )
                    )

    return _build_content_vulnerabilities(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.SUB_RESOURCE_INTEGRITY,
    )


def _view_state(ctx: ContentCheckCtx) -> Vulnerabilities:
    locations: list[Location] = []

    for tag in ctx.url_ctx.soup.find_all("input"):
        if tag.get("name") == "__VIEWSTATE" and (value := tag.get("value")):
            with contextlib.suppress(viewstate.ViewStateException):
                view_state = viewstate.ViewState(base64=value)
                view_state.decode()

                locations.append(
                    Location.from_soup_tag(
                        desc="view_state.not_encrypted",
                        tag=tag,
                    )
                )

    return _build_content_vulnerabilities(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.VIEW_STATE,
    )


def get_check_ctx(url: URLContext) -> ContentCheckCtx:
    return ContentCheckCtx(
        url_ctx=url,
    )


CHECKS: dict[
    FindingEnum,
    list[Callable[[ContentCheckCtx], Vulnerabilities]],
] = {
    FindingEnum.F036: [_view_state],
    FindingEnum.F086: [_sub_resource_integrity],
}
