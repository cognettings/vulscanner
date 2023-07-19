from androguard.core.analysis.analysis import (
    Analysis,
)
from androguard.core.bytecodes.apk import (
    APK,
)
from androguard.core.bytecodes.dvm import (
    DalvikVMFormat,
)
from androguard.decompiler.decompiler import (
    DecompilerDAD,
)
from bs4 import (
    BeautifulSoup,
)
import contextlib
import lxml.etree  # nosec
from model.core import (
    LocalesEnum,
    MethodsEnum,
    Vulnerabilities,
)
from typing import (
    NamedTuple,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
import zipfile
from zone import (
    t,
)


class APKContext(NamedTuple):
    analysis: Analysis | None
    apk_manifest: BeautifulSoup | None
    apk_obj: APK | None
    path: str


class APKCheckCtx(NamedTuple):
    apk_ctx: APKContext


class Location(NamedTuple):
    description: str
    snippet: str
    vuln_line: str | None = None
    details: str | None = None


class Locations(NamedTuple):
    locations: list[Location]

    def append(
        self,
        desc: str,
        snippet: str,
        vuln_line: str | None = None,
        details: str | None = None,
        **desc_kwargs: LocalesEnum | str,
    ) -> None:
        self.locations.append(
            Location(
                description=t(
                    f"lib_apk.analyze_bytecodes.{desc}",
                    **desc_kwargs,
                ),
                snippet=snippet,
                vuln_line=vuln_line,
                details=details,
            )
        )


def create_vulns(
    ctx: APKCheckCtx,
    locations: Locations,
    method: MethodsEnum,
) -> Vulnerabilities:
    return tuple(
        build_lines_vuln(
            method=method,
            what=ctx.apk_ctx.path
            + (f" (Details: {location.details})" if location.details else ""),
            where=location.vuln_line if location.vuln_line else "0",
            metadata=build_metadata(
                method=method,
                description=location.description,
                snippet=location.snippet,
            ),
        )
        for location in locations.locations
    )


def get_apk_context(path: str) -> APKContext:
    apk_obj: APK | None = None
    apk_manifest: BeautifulSoup | None = None
    analysis: Analysis | None = None
    with contextlib.suppress(zipfile.BadZipFile):
        apk_obj = APK(path)

        with contextlib.suppress(KeyError):
            apk_manifest_data = apk_obj.xml["AndroidManifest.xml"]
            apk_manifest = BeautifulSoup(
                BeautifulSoup(
                    # pylint: disable=c-extension-no-member
                    lxml.etree.tostring(apk_manifest_data),
                    features="html.parser",
                ).prettify(),
                features="html.parser",
            )

        dalviks = []
        analysis = Analysis()
        for dex in apk_obj.get_all_dex():
            dalvik = DalvikVMFormat(
                dex,
                using_api=apk_obj.get_target_sdk_version(),
            )
            analysis.add(dalvik)
            dalviks.append(dalvik)
            dalvik.set_decompiler(DecompilerDAD(dalviks, analysis))

        analysis.create_xref()

    return APKContext(
        analysis=analysis,
        apk_manifest=apk_manifest,
        apk_obj=apk_obj,
        path=path,
    )


def get_check_ctx(apk_ctx: APKContext) -> APKCheckCtx:
    return APKCheckCtx(
        apk_ctx=apk_ctx,
    )
