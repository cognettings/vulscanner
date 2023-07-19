from .apk_utils import (
    APKCheckCtx,
    create_vulns,
    Locations,
)
from bs4 import (
    BeautifulSoup,
    Tag,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)


def _add_android_manifest_location(
    *,
    apk_manifest: BeautifulSoup,
    desc: str,
    locations: Locations,
    column: int,
    line: int,
    details: str | None = None,
    **desc_kwargs: str,
) -> None:
    locations.append(
        desc=desc,
        vuln_line="0",
        snippet=make_snippet(
            content=apk_manifest.prettify(),
            viewport=SnippetViewport(
                column=column,
                line=line,
                wrap=True,
            ),
        ).content,
        details=details,
        **desc_kwargs,
    )


def _get_caseless_attr(tag: Tag, key: str, default: str) -> str:
    attr: str
    key = key.lower()
    for attr, value in tag.attrs.items():
        if attr.lower() == key:
            return value
    return default


def apk_backups_enabled(
    ctx: APKCheckCtx,
) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_manifest is None:
        return ()

    application: Tag
    for application in ctx.apk_ctx.apk_manifest.find_all("application"):
        allows_backup: str = _get_caseless_attr(
            application,
            key="android:allowBackup",
            default="not-set",
        ).lower()

        if allows_backup == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="backups_enabled",
                locations=locations,
                column=application.sourcepos,
                line=application.sourceline,
                details=f"Line {application.sourceline} with backups enabled",
            )
        elif allows_backup == "not-set":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="backups_not_configured",
                locations=locations,
                column=0,
                line=0,
            )

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.APK_BACKUPS_ENABLED,
    )


def apk_debugging_enabled(
    ctx: APKCheckCtx,
) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_manifest is None:
        return ()

    application: Tag
    for application in ctx.apk_ctx.apk_manifest.find_all("application"):
        is_debuggable: str = _get_caseless_attr(
            application,
            key="android:debuggable",
            default="false",
        ).lower()

        if is_debuggable == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="debugging_enabled",
                locations=locations,
                column=application.sourcepos,
                line=application.sourceline,
                details=(
                    f"Line {application.sourceline} with debugging enabled"
                ),
            )

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.APK_DEBUGGING_ENABLED,
    )


def apk_exported_cp(
    ctx: APKCheckCtx,
) -> Vulnerabilities:
    if ctx.apk_ctx.apk_manifest is None:
        return ()

    locations: Locations = Locations([])

    provider: Tag
    for provider in ctx.apk_ctx.apk_manifest.find_all("provider"):
        authority: str = _get_caseless_attr(
            provider,
            key="android:authorities",
            default="",
        ) or _get_caseless_attr(
            provider,
            key="android:name",
            default="",
        )
        exported: str = _get_caseless_attr(
            provider,
            key="android:exported",
            default="false",
        ).lower()
        grant_uri_permissions: str = _get_caseless_attr(
            provider,
            key="android:grantUriPermissions",
            default="false",
        ).lower()

        if exported == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="exported",
                desc_authority=authority,
                locations=locations,
                column=provider.sourcepos,
                line=provider.sourceline,
                details=f"Line {provider.sourceline} with android:exported",
            )
        if grant_uri_permissions == "true":
            _add_android_manifest_location(
                apk_manifest=ctx.apk_ctx.apk_manifest,
                desc="grants_uri_permissions",
                desc_authority=authority,
                locations=locations,
                column=provider.sourcepos,
                line=provider.sourceline,
                details=f"Line {provider.sourceline} with grantUriPermissions",
            )

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.APK_EXPORTED_CP,
    )
