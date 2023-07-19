from .analyze_manifest import (
    apk_backups_enabled,
    apk_debugging_enabled,
    apk_exported_cp,
)
from .apk_utils import (
    APKCheckCtx,
    create_vulns,
    Locations,
)
import androguard
from androguard.core.bytecodes.axml import (
    AXMLPrinter,
)
from androguard.core.bytecodes.dvm import (
    ClassDefItem,
    DalvikVMFormat,
)
from bs4 import (
    BeautifulSoup,
)
from collections.abc import (
    Callable,
    Iterable,
)
import lxml.etree  # nosec
from model.core import (
    FindingEnum,
    MethodsEnum,
    Vulnerabilities,
)
from operator import (
    attrgetter,
)
import re
from serializers import (
    make_snippet,
    SnippetViewport,
)
import textwrap


def is_method_present(
    dex: DalvikVMFormat, class_name: str, method: str, descriptor: str
) -> list[str]:
    """Search if method is present in decompiled code."""
    met_ana = dex.get_method_analysis_by_name(
        class_name=class_name, method_name=method, method_descriptor=descriptor
    )

    if not met_ana:
        return []

    used_by = [
        x.name for x, _, _ in met_ana.get_xref_from() if "Activity" in x.name
    ]

    return used_by


def get_activities_source(dvms: list) -> str:
    """Decompile given Dalvik VM images."""
    source = [
        x.get_source()
        for dvm in dvms
        for x in dvm.get_classes()
        if "Activity" in x.name
    ]
    return "".join(source)


def _add_apk_unsigned_not_signed_location(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="apk_unsigned",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # Check the META-INF/ folder and retrieve signature pairs
                >>> # with extensions: .DSA & .DF, .EC & .DF, or .RSA & .DF
                >>> apk.get_signature_names()
                []  # Empty list means no signatures exist
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=12, wrap=True),
        ).content,
    )


def _apk_unsigned(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_obj is not None:
        signatures: list[str] = ctx.apk_ctx.apk_obj.get_signature_names()

        if not signatures:
            _add_apk_unsigned_not_signed_location(ctx, locations)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.APK_UNSIGNED,
    )


def _add_no_root_check_location(
    ctx: APKCheckCtx,
    locations: Locations,
    methods: Iterable[str],
) -> None:
    locations.append(
        desc="no_root_check",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse all Dalvik Executables (classes*.dex) in the APK
                >>> dex = AnalyzeAPK({repr(ctx.apk_ctx.path)})[2]

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
        ).content,
    )


def _get_method_names(
    get_analysis: androguard.core.analysis.analysis.Analysis,
) -> list[str]:
    names: list[str] = sorted(
        set(map(attrgetter("name"), get_analysis.get_methods()))
    )

    return names


def _no_root_check(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        method_names: list[str] = _get_method_names(ctx.apk_ctx.analysis)

        if not any(
            method_name
            in {
                "checkForBusyBoxBinary",
                "checkForDangerousProps",
                "checkForSuBinary",
                "checkSuExists",
                "isRooted",
                "isRootedExperimentalAsync",
            }
            for method_name in method_names
        ):
            _add_no_root_check_location(ctx, locations, method_names)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.NO_ROOT_CHECK,
    )


def _get_class_names(
    get_analysis: androguard.core.analysis.analysis.Analysis,
) -> list[str]:
    names: list[str] = sorted(
        set(map(attrgetter("name"), get_analysis.get_classes()))
    )

    return names


def _add_no_certs_pinning_1_location(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="no_certs_pinning_config",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # List all files in the APK
                >>> apk_files = apk.zip.nameslist()
                >>> "res/xml/network_security_config.xml" in apk_files
                False  # No network security config exists
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=11, wrap=True),
        ).content,
    )


def _add_no_certs_pinning_2_location(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="no_certs_pinning",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK
                >>> # and version 4.9.3 of "beautifulsoup4"
                >>> from bs4 import BeautifulSoup

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # Read and parse the Network Security Config manifest
                >>> nsc = apk.get_file("res/xml/network_security_config.xml")
                >>> BeautifulSoup(nsc).find_all("pin-set")
                []  # Empty list means no <pin-set> tags were defined
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=13, wrap=True),
        ).content,
    )


def _no_certs_pinning(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])
    if (
        ctx.apk_ctx.apk_obj is not None
        and ctx.apk_ctx.analysis is not None
        and (
            "Lcom/toyberman/RNSslPinningModule;"
            not in _get_class_names(ctx.apk_ctx.analysis)
        )
    ):
        try:
            nsc: str = "res/xml/network_security_config.xml"
            nsc_content: bytes = ctx.apk_ctx.apk_obj.zip.read(nsc)
        except KeyError:
            # No network security config exists
            _add_no_certs_pinning_1_location(ctx, locations)
        else:
            xml_object = AXMLPrinter(nsc_content).get_xml_obj()
            nsc_parsed = BeautifulSoup(
                BeautifulSoup(
                    # pylint: disable=c-extension-no-member
                    lxml.etree.tostring(xml_object),
                    features="html.parser",
                ).prettify(),
                features="html.parser",
            )
            if not list(nsc_parsed.find_all("pin-set")):
                # No pin sets exist
                _add_no_certs_pinning_2_location(ctx, locations)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.NO_CERTS_PINNING,
    )


def _add_no_obfuscation_location(
    class_name: str,
    class_source: str,
    locations: Locations,
) -> None:
    locations.append(
        desc="no_obfuscation",
        desc_class_name=class_name,
        snippet=make_snippet(
            content=class_source,
            viewport=SnippetViewport(column=0, line=1, wrap=True),
        ).content,
        details=f"Non obfuscated class {class_name}",
    )


def _no_obfuscation(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    class_names_unobfuscated: set[str] = {
        "androidx/annotation/",
        "javax/inject/",
        "androidx/browser/",
        "androidx/viewpager2/",
        "de/greenrobot/",
        "androidx/savedstate/",
        "androidx/media/",
        "butterknife/internal/",
        "androidx/activity/",
        "me/leolin/",
        "androidx/versionedparcelable/",
        "io/nlopez/",
        "butterknife/runtime/",
        "org/unimodules/",
        "androidx/cardview/",
        "com/raizlabs/",
        "androidx/coordinatorlayout/",
        "androidx/viewpager/",
        "androidx/lifecycle/",
        "android/support/",
        "net/openid/",
        "com/amplitude/",
        "androidx/biometric/",
        "com/theartofdev/",
        "androidx/core/",
        "androidx/fragment/",
        "okhttp3/internal/",
        "androidx/recyclerview/",
        "host/exp/",
        "com/bumptech/",
        "androidx/appcompat/",
        "versioned/host/",
        "expo/modules/",
        "com/google/",
        "com/facebook/",
    }

    if ctx.apk_ctx.analysis is not None:
        dvms: DalvikVMFormat
        for dvms in ctx.apk_ctx.analysis.vms:
            class_: ClassDefItem
            for class_ in dvms.get_classes():
                class_name: str = class_.get_name()[1:-1]
                class_is_interface: bool = 0x200 & class_.get_access_flags()
                if not class_is_interface and any(
                    map(class_name.startswith, class_names_unobfuscated)
                ):
                    _add_no_obfuscation_location(
                        class_name=class_name,
                        class_source=class_.get_source(),
                        locations=locations,
                    )
                    break

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.NO_OBFUSCATION,
    )


def _add_has_fragment_injection_location(
    ctx: APKCheckCtx,
    locations: Locations,
    source: str,
    target_sdk_version: int,
) -> None:
    locations.append(
        desc="has_fragment_injection",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> apk_obj, dex, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the targetSdkVersion attribute
                >>> apk_obj.get_target_sdk_version()
                >>> {repr(target_sdk_version)}
                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
        ).content,
    )


def _has_fragment_injection(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.apk_obj is not None and ctx.apk_ctx.analysis is not None:
        sdk_version = ctx.apk_ctx.apk_obj.get_target_sdk_version()
        target_sdk_version = int(sdk_version) if sdk_version else 0

        act_source = get_activities_source(ctx.apk_ctx.analysis.vms)

        is_vulnerable: bool = (
            target_sdk_version < 19 and "PreferenceActivity" in act_source
        )

        if is_vulnerable:
            _add_has_fragment_injection_location(
                ctx, locations, act_source, target_sdk_version
            )

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.FRAGMENT_INJECTION,
    )


def _add_webview_allows_resource_access(
    ctx: APKCheckCtx,
    locations: Locations,
    source: Iterable[str],
) -> None:
    locations.append(
        desc="webview_allows_resource_access",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> _, dex, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # The setJavaScriptEnabled method and the following dangerous
                # methods are enabled:
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=14, wrap=True),
        ).content,
        details="Allow dangerous resource access",
    )


def _add_webview_caches_javascript_location(
    ctx: APKCheckCtx,
    locations: Locations,
    source: str,
) -> None:
    locations.append(
        desc="webview_caches_javascript",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> _, dex, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # The setJavaScriptEnabled method is enabled and the clearCache
                # method is not present.
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=12, wrap=True),
        ).content,
        details="clearCache not used with JS enabled",
    )


def _webview_vulnerabilities(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    dangerous_allows = {
        "setAllowContentAccess",
        "setAllowFileAccess",
        "setAllowFileAccessFromFileURLs",
        "setAllowUniversalAccessFromFileURLs",
    }

    if ctx.apk_ctx.analysis is not None:
        act_source = get_activities_source(ctx.apk_ctx.analysis.vms)
        effective_dangerous: list[str] = []

        if "setJavaScriptEnabled" in act_source:
            if "clearCache" not in act_source:
                _add_webview_caches_javascript_location(
                    ctx, locations, act_source
                )

            effective_dangerous = list(
                filter(act_source.__contains__, dangerous_allows)
            )

        if bool(effective_dangerous):
            _add_webview_allows_resource_access(
                ctx, locations, effective_dangerous
            )

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.WEBVIEW_VULNS,
    )


def _add_has_frida(
    ctx: APKCheckCtx, locations: Locations, source: Iterable[str]
) -> None:
    locations.append(
        desc="has_frida",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> apk_obj, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the files attribute
                >>> apk_obj.get_files()
                # No method performs root detection
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=13, wrap=True),
        ).content,
    )


def _has_frida(
    ctx: APKCheckCtx,
) -> Vulnerabilities:
    locations: Locations = Locations([])

    apk_obj = ctx.apk_ctx.apk_obj
    if not apk_obj:
        return create_vulns(
            ctx=ctx,
            locations=locations,
            method=MethodsEnum.HAS_FRIDA,
        )
    frida_gadgets: list[str] = [x for x in apk_obj.get_files() if "frida" in x]
    is_frida_gadget_in_files: bool = bool(frida_gadgets)

    if is_frida_gadget_in_files:
        _add_has_frida(ctx, locations, apk_obj.get_files())

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.HAS_FRIDA,
    )


def _add_not_verifies_ssl_hostname(
    ctx: APKCheckCtx,
    locations: Locations,
    source: str,
) -> None:
    locations.append(
        desc="not_verifies_ssl_hostname",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse APK and all Dalvik Executables (classes*.dex)
                >>> # in the APK
                >>> _, dex, _ = AnalyzeAPK({repr(ctx.apk_ctx.path)})

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                >>> {repr(source)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=12, wrap=True),
        ).content,
    )


def _not_verifies_ssl_hostname(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        act_source = get_activities_source(ctx.apk_ctx.analysis.vms)
        is_vulnerable: bool = False

        if (
            "SSLSocket" in act_source
            and "getDefaultHostnameVerifier" not in act_source
        ):
            is_vulnerable = True

        if is_vulnerable:
            _add_not_verifies_ssl_hostname(ctx, locations, act_source)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.NOT_VERIFIES_SSL_HOSTNAME,
    )


def _add_uses_insecure_delete(
    ctx: APKCheckCtx,
    locations: Locations,
    methods: Iterable[str],
) -> None:
    locations.append(
        desc="uses_insecure_delete",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse all Dalvik Executables (classes*.dex) in the APK
                >>> dex = AnalyzeAPK({repr(ctx.apk_ctx.path)})[2]

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                 >>> {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
        ).content,
    )


def _uses_insecure_delete(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        dex = ctx.apk_ctx.analysis
        method_names: list[str] = _get_method_names(ctx.apk_ctx.analysis)

        deletes_insecure: list[str] = is_method_present(
            dex, "Ljava/io/File;", "delete", "()Z"
        )

        if deletes_insecure:
            _add_uses_insecure_delete(ctx, locations, method_names)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.USES_INSECURE_DELETE,
    )


def _add_uses_http_resources(
    ctx: APKCheckCtx,
    locations: Locations,
    methods: Iterable[str],
) -> None:
    locations.append(
        desc="uses_http_resources",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse all Dalvik Executables (classes*.dex) in the APK
                >>> dex = AnalyzeAPK({repr(ctx.apk_ctx.path)})[2]

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # HTTP resources found
                 >>> {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
        ).content,
    )


def _uses_http_resources(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    whitelist = {
        "http://schemas.android.com/",
        "http://www.w3.org/",
        "http://apache.org/",
        "http://xml.org/",
        "http://localhost/",
        "http://localhost",
        "http://127.0.0.1/",
        "http://java.sun.com/",
        r"http:\/\/\[",
    }

    if ctx.apk_ctx.analysis is not None:
        dex = ctx.apk_ctx.analysis

        insecure_urls = [
            x.get_value()
            for x in dex.get_strings()
            if re.match(r"^http?\:\/\/.+", x.get_value())
            and not any(
                re.match(whitel, x.get_value()) for whitel in whitelist
            )
        ]

        if insecure_urls:
            _add_uses_http_resources(ctx, locations, insecure_urls)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.USES_HTTP_RESOURCES,
    )


def _add_allow_user_ca_by_default(
    ctx: APKCheckCtx,
    locations: Locations,
) -> None:
    locations.append(
        desc="allow_user_ca_by_default",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # Get SDK version
                >>> apk.get_target_sdk_version()
                >>> No network security config file found and SDK version
                >>> allows user-supplied CAs by default
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=10, wrap=True),
        ).content,
    )


def _add_allow_user_ca(
    ctx: APKCheckCtx,
    locations: Locations,
    methods: str,
) -> None:
    locations.append(
        desc="allow_user_ca",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.core.bytecodes.apk import APK

                >>> # This object represents the APK to analyze
                >>> apk = APK({repr(ctx.apk_ctx.path)})

                >>> # Get network security config file
                >>> apk.get_file("res/xml/network_security_config.xml")()
                >>> {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=11, wrap=True),
        ).content,
    )


def _improper_certificate_validation(
    ctx: APKCheckCtx,
) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None and (apk_obj := ctx.apk_ctx.apk_obj):
        net_conf: str = ""

        try:
            net_conf = str(
                apk_obj.get_file("res/xml/network_security_config.xml")
            )
        except androguard.core.bytecodes.apk.FileNotPresent:
            sdk_version = apk_obj.get_target_sdk_version()
            target_sdk = int(sdk_version) if sdk_version else 0
            if target_sdk < 24:
                _add_allow_user_ca_by_default(ctx, locations)

        if "trust-anchors" in net_conf and "user" in net_conf:
            _add_allow_user_ca(ctx, locations, net_conf)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.IMPROPER_CERTIFICATE_VALIDATION,
    )


def _add_socket_uses_get_insecure(
    ctx: APKCheckCtx,
    locations: Locations,
    methods: Iterable[str],
) -> None:
    locations.append(
        desc="uses_get_insecure",
        snippet=make_snippet(
            content=textwrap.dedent(
                f"""
                $ python3.11

                >>> # We'll use the version 3.3.5 of "androguard"
                >>> from androguard.misc import AnalyzeAPK

                >>> # Parse all Dalvik Executables (classes*.dex) in the APK
                >>> dex = AnalyzeAPK({repr(ctx.apk_ctx.path)})[2]

                >>> # Get the method names from all classes in each .dex file
                >>> sorted(set(method.name for method in dex.get_methods()))
                # No method performs root detection
                 >>> {repr(methods)}
                """
            )[1:],
            viewport=SnippetViewport(column=0, line=12, wrap=True),
        ).content,
    )


def _uses_insecure_sockets(ctx: APKCheckCtx) -> Vulnerabilities:
    locations: Locations = Locations([])

    if ctx.apk_ctx.analysis is not None:
        dex = ctx.apk_ctx.analysis
        method_names: list[str] = _get_method_names(ctx.apk_ctx.analysis)

        uses_get_insecure: list[str] = is_method_present(
            dex=dex,
            class_name="Landroid/net/SSLCertificateSocketFactory;",
            method="getInsecure",
            descriptor=(
                "(I Landroid/net/SSLSessionCache;)"
                "Ljavax/net/ssl/SSLSocketFactory;"
            ),
        )

        if uses_get_insecure:
            _add_socket_uses_get_insecure(ctx, locations, method_names)

    return create_vulns(
        ctx=ctx,
        locations=locations,
        method=MethodsEnum.SOCKET_GET_INSECURE,
    )


CHECKS: dict[
    FindingEnum,
    list[Callable[[APKCheckCtx], Vulnerabilities]],
] = {
    FindingEnum.F046: [_no_obfuscation],
    FindingEnum.F048: [_no_root_check],
    FindingEnum.F055: [apk_backups_enabled],
    FindingEnum.F058: [apk_debugging_enabled],
    FindingEnum.F060: [_not_verifies_ssl_hostname],
    FindingEnum.F075: [apk_exported_cp],
    FindingEnum.F082: [
        _uses_insecure_delete,
        _uses_insecure_sockets,
    ],
    FindingEnum.F103: [_apk_unsigned],
    FindingEnum.F206: [_has_frida],
    FindingEnum.F207: [_no_certs_pinning],
    FindingEnum.F268: [_webview_vulnerabilities],
    FindingEnum.F313: [_improper_certificate_validation],
    FindingEnum.F398: [_has_fragment_injection],
}
