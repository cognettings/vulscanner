from collections.abc import (
    Callable,
    Iterable,
)
import ctx as skims_ctx
from lib.ssl.as_string import (
    snippet,
    ssl_id2ssl_name,
)
from lib.ssl.ssl_connection import (
    get_client_hello_package,
    get_ec_point_formats_ext,
    get_elliptic_curves_ext,
    get_heartbeat_ext,
    get_malicious_heartbeat,
    get_session_ticket_ext,
    parse_server_response,
    read_ssl_record,
    ssl_connect,
)
from lib.ssl.suites import (
    get_suite_by_openssl_name,
    get_suites_with_cbc,
    get_suites_with_pfs,
    get_weak_suites,
    SSLCipherSuite,
    SSLSpecialSuite,
    SSLSuiteInfo,
    SSLVersionId,
)
from lib.ssl.types import (
    SSLContext,
    SSLHandshakeRecord,
    SSLRecord,
    SSLServerHandshake,
    SSLServerResponse,
    SSLSettings,
    SSLVulnerability,
)
from model import (
    core,
)
from utils.sockets import (
    tcp_connect,
)
from vulnerabilities import (
    build_inputs_vuln,
    build_metadata,
)
from zone import (
    t,
)


def tls_connect(
    host: str, port: int, v_id: SSLVersionId
) -> SSLServerResponse | None:
    intention_en = "verify if server supports " + ssl_id2ssl_name(v_id)
    ssl_settings = SSLSettings(
        context=SSLContext(host=host, port=port),
        tls_version=v_id,
        intention={core.LocalesEnum.EN: intention_en},
    )

    with ssl_connect(ssl_settings) as ssl_socket:
        if ssl_socket is not None and (cipher_info := ssl_socket.cipher()):
            openssl_name, _, _ = cipher_info
            return SSLServerResponse(
                record=SSLRecord.HANDSHAKE,
                version_id=v_id,
                handshake=SSLServerHandshake(
                    record=SSLHandshakeRecord.SERVER_HELLO,
                    version_id=v_id,
                    cipher_suite=get_suite_by_openssl_name(openssl_name),
                ),
            )
    return None


def _create_core_vulns(
    *,
    ssl_vulnerabilities: Iterable[SSLVulnerability],
) -> core.Vulnerabilities:
    return tuple(
        build_inputs_vuln(
            method=ssl_vulnerability.method,
            stream="home,socket-send,socket-response",
            what=str(ssl_vulnerability)
            if str(ssl_vulnerability).startswith(("https://", "http://"))
            else f"https://{str(ssl_vulnerability)}",
            where=ssl_vulnerability.description,
            metadata=build_metadata(
                method=ssl_vulnerability.method,
                description=ssl_vulnerability.description,
                snippet=snippet(
                    locale=skims_ctx.SKIMS_CONFIG.language,
                    ssl_vulnerability=ssl_vulnerability,
                ),
            ),
        )
        for ssl_vulnerability in ssl_vulnerabilities
    )


def _create_ssl_vuln(
    ssl_settings: SSLSettings,
    server_response: SSLServerResponse | None,
    method: core.MethodsEnum,
    check_kwargs: dict[str, str | core.LocalesEnum] | None = None,
) -> SSLVulnerability:
    return SSLVulnerability(
        ssl_settings=ssl_settings,
        server_response=server_response,
        description=t(
            f"lib_ssl.analyze_protocol.{method.value.name}",
            **(check_kwargs or {}),
        ),
        method=method,
    )


def _pfs_disabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: list[SSLSuiteInfo] = list(get_suites_with_pfs())

    extensions: list[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()

    en_intention = (
        "Perform a {v_name} request offering only key exchange algorithms\n"
        "with PFS support and check if the connection is accepted by the\n"
        "server"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo únicamente algoritmos\n"
        "de intercambio de llaves con soporte PFS y verificar si la conexión\n"
        "es aceptada por el servidor"
    )

    for v_id in tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue

        intention: dict[core.LocalesEnum, str] = {
            core.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core.LocalesEnum.ES: (
                es_intention.format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(
            v_id=v_id,
            cipher_suites=suites,
            host=ctx.host,
            extensions=extensions,
        )
        sock.send(bytes(package))
        response: SSLServerResponse | None = parse_server_response(sock)

        if response is not None and response.alert is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        key_exchange_names=[
                            "DHE",
                            "ECDHE",
                            "SRP",
                            "ECCPWD",
                        ],
                        intention=intention,
                    ),
                    server_response=response,
                    method=core.MethodsEnum.PFS_DISABLED,
                    check_kwargs={"v_name": ssl_id2ssl_name(v_id)},
                )
            )

        sock.close()

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _sslv3_enabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []

    suites: list[SSLSuiteInfo] = [
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.RSA_PSK_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_IDEA_CBC_SHA.value,
        SSLCipherSuite.RSA_PSK_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_RC4_128_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_66.value,
        SSLCipherSuite.ECDH_anon_WITH_RC4_128_SHA.value,
        SSLCipherSuite.DH_anon_WITH_RC4_128_MD5.value,
        SSLCipherSuite.ECDH_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_MD5.value,
        SSLCipherSuite.RSA_PSK_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_PSK_WITH_3DES_EDE_CBC_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_63.value,
        SSLCipherSuite.DHE_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DH_anon_WITH_DES_CBC_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_62.value,
        SSLCipherSuite.RSA_WITH_DES_CBC_SHA.value,
        SSLSpecialSuite.RESERVED_SUITE_00_61.value,
        SSLSpecialSuite.RESERVED_SUITE_00_65.value,
        SSLSpecialSuite.RESERVED_SUITE_00_64.value,
        SSLSpecialSuite.RESERVED_SUITE_00_60.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DH_anon_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.DH_anon_EXPORT_WITH_RC4_40_MD5.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLCipherSuite.ECDHE_RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDH_anon_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_NULL_SHA.value,
        SSLCipherSuite.RSA_WITH_NULL_SHA.value,
        SSLCipherSuite.RSA_WITH_NULL_MD5.value,
        SSLSpecialSuite.EMPTY_RENEGOTIATION_INFO_SCSV.value,
    ]

    en_intention = (
        "Perform a SSLv3 request offering any cipher suite and check if the\n"
        "connection is accepted by the server"
    )

    es_intention = (
        "Realizar una petición SSLv3 ofreciendo cualquier suite de cifrado\n"
        "y verificar si la conexión es aceptada por el servidor"
    )

    intention: dict[core.LocalesEnum, str] = {
        core.LocalesEnum.EN: en_intention,
        core.LocalesEnum.ES: es_intention,
    }

    sock = tcp_connect(
        ctx.host,
        ctx.port,
        intention[core.LocalesEnum.EN],
    )

    if sock is None:
        return tuple()

    package = get_client_hello_package(
        v_id=SSLVersionId.sslv3_0,
        cipher_suites=suites,
        host=ctx.host,
    )
    sock.send(bytes(package))
    response: SSLServerResponse | None = parse_server_response(sock)

    if response is not None and response.handshake is not None:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.sslv3_0,
                    intention=intention,
                ),
                server_response=response,
                method=core.MethodsEnum.SSLV3_ENABLED,
            )
        )
    sock.close()

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _tlsv1_enabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    en_intention = (
        "Perform a TLSv1.0 request offering any cipher suite and check if\n"
        "the server accepts the connection"
    )

    es_intention = (
        "Realizar una petición TLSv1.0 ofreciendo cualquier suite de\n"
        "cifrado y verificar si el servidor acepta la conexión"
    )

    if SSLVersionId.tlsv1_0 in tls_versions:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.tlsv1_0,
                    intention={
                        core.LocalesEnum.EN: en_intention,
                        core.LocalesEnum.ES: es_intention,
                    },
                ),
                server_response=ctx.get_tls_response(SSLVersionId.tlsv1_0),
                method=core.MethodsEnum.TLSV1_ENABLED,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _tlsv1_1_enabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    en_intention = (
        "Perform a TLSv1.1 request offering any cipher suite and check if\n"
        "the server accepts the connection"
    )

    es_intention = (
        "Realizar una petición TLSv1.1 ofreciendo cualquier suite de\n"
        "cifrado y verificar si el servidor acepta la conexión"
    )

    if SSLVersionId.tlsv1_1 in tls_versions:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.tlsv1_1,
                    intention={
                        core.LocalesEnum.EN: en_intention,
                        core.LocalesEnum.ES: es_intention,
                    },
                ),
                server_response=ctx.get_tls_response(SSLVersionId.tlsv1_1),
                method=core.MethodsEnum.TLSV1_1_ENABLED,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _tlsv1_2_or_higher_disabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    if not tls_versions:
        return tuple()

    en_intention = (
        "Perform a request offering any cipher suite on versions TLSv1.2 or\n"
        "TLSv1.3 and check if the server accepts the connection"
    )

    es_intention = (
        "Realizar una petición ofreciendo cualquier suite de cifrado con\n"
        "las versiones TLSv1.2 o TLSv1.3 y verificar si el servidor acepta\n"
        "la conexión"
    )

    if (
        SSLVersionId.tlsv1_2 not in tls_versions
        and SSLVersionId.tlsv1_3 not in tls_versions
    ):
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=SSLVersionId.tlsv1_3,
                    intention={
                        core.LocalesEnum.EN: en_intention,
                        core.LocalesEnum.ES: es_intention,
                    },
                ),
                server_response=None,
                method=core.MethodsEnum.TLSV1_2_OR_HIGHER_DISABLED,
            )
        )

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


# pylint: disable=too-many-arguments
def _get_weak_enabled_suites_as_vuln(
    ctx: SSLContext,
    v_id: SSLVersionId,
    cipher_suites: Iterable[SSLSuiteInfo],
    intention: dict[core.LocalesEnum, str],
    method: core.MethodsEnum,
    cipher_names: Iterable[str],
    hash_names: Iterable[str],
    extensions: Iterable[int] | None = None,
) -> list[SSLVulnerability]:
    ssl_vulnerabilities: list[SSLVulnerability] = []

    for suite in cipher_suites:
        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core.LocalesEnum.EN],
        )

        if sock is None:
            continue

        package = get_client_hello_package(
            v_id=v_id,
            cipher_suites=[suite],
            host=ctx.host,
            extensions=extensions,
        )

        sock.send(bytes(package))
        response: SSLServerResponse | None = parse_server_response(sock)

        if (
            response is not None
            and response.handshake is not None
            and response.handshake.cipher_suite is not None
        ):
            cipher_iana_name = response.handshake.cipher_suite.iana_name
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        cipher_names=list(cipher_names),
                        hash_names=list(hash_names),
                        intention=intention,
                    ),
                    server_response=response,
                    method=method,
                    check_kwargs={
                        "v_name": ssl_id2ssl_name(v_id),
                        "insecure_cipher": cipher_iana_name,
                    },
                )
            )

        sock.close()

    return ssl_vulnerabilities


def _weak_ciphers_allowed(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()
    suites: list[SSLSuiteInfo] = list(get_weak_suites())
    cipher_names: list[str] = [
        "NULL",
        "RC2",
        "RC4",
        "DES",
        "DES3",
        "SM3",
        "SM4",
    ]
    hash_names: list[str] = [
        "SHA",
        "MD5",
        "SM3",
    ]
    en_intention = (
        "Perform a {v_name} request offering only weak cipher suites and\n"
        "check if the connection is accepted by the server"
    )
    es_intention = (
        "Realizar una petición {v_name} ofreciendo solamente suites de\n"
        "cifrado débiles y verificar si la conexión es aceptada por el\n"
        "servidor"
    )

    for v_id in tls_versions:
        intention: dict[core.LocalesEnum, str] = {
            core.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }
        ssl_vulnerabilities += _get_weak_enabled_suites_as_vuln(
            ctx,
            v_id,
            suites,
            intention,
            core.MethodsEnum.WEAK_CIPHERS_ALLOWED,
            cipher_names,
            hash_names,
        )

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _cbc_enabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()
    suites: list[SSLSuiteInfo] = list(get_suites_with_cbc())
    extensions: list[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    cipher_names: list[str] = [
        "CBC",
    ]
    hash_names: list[str] = [
        "ANY",
    ]
    en_intention = (
        "Perform a {v_name} request offering any cipher suite \n"
        "and check if the connection is accepted by the server"
    )
    es_intention = (
        "Realizar una petición {v_name} ofreciendo solamente suites de\n"
        "cifrado que usen CBC y verificar si la conexión es aceptada por el\n"
        "servidor"
    )

    for v_id in tls_versions:
        if v_id == SSLVersionId.tlsv1_3:
            continue
        intention: dict[core.LocalesEnum, str] = {
            core.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }
        ssl_vulnerabilities += _get_weak_enabled_suites_as_vuln(
            ctx,
            v_id,
            suites,
            intention,
            core.MethodsEnum.CBC_ENABLED,
            cipher_names,
            hash_names,
            extensions,
        )

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _fallback_scsv_disabled(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()
    if tls_versions:
        min_v_id: SSLVersionId = min(tls_versions)
    else:
        return tuple()

    if min_v_id == SSLVersionId.tlsv1_2 or len(tls_versions) < 2:
        return tuple()

    suites: list[SSLSuiteInfo] = [
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_CHACHA20_POLY1305_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA384.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA384.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_256_GCM_SHA384.value,
        SSLCipherSuite.RSA_WITH_AES_128_GCM_SHA256.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA256.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA256.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA.value,
        SSLSpecialSuite.FALLBACK_SCSV.value,
    ]

    en_intention = (
        "Perform a request with the lower TLS version supported by the\n"
        "server with the TLS_FALLBACK_SCSV parameter set on true and check\n"
        "if the server accept the connection"
    )

    es_intention = (
        "Realizar una petición con la menor versión de TLS soportada por el\n"
        "servidor con el paremtro TLS_FALLBACK_SCSV activado y verificar si\n"
        "el servidor acepta la conexión"
    )

    intention: dict[core.LocalesEnum, str] = {
        core.LocalesEnum.EN: en_intention,
        core.LocalesEnum.ES: es_intention,
    }

    sock = tcp_connect(
        ctx.host,
        ctx.port,
        intention[core.LocalesEnum.EN],
    )

    if sock is None:
        return tuple()

    extensions: list[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()

    package = get_client_hello_package(
        v_id=min_v_id,
        cipher_suites=suites,
        host=ctx.host,
        extensions=extensions,
    )
    sock.send(bytes(package))
    response: SSLServerResponse | None = parse_server_response(sock)

    if response is not None and response.handshake is not None:
        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                ssl_settings=SSLSettings(
                    context=ctx,
                    tls_version=min_v_id,
                    intention=intention,
                ),
                server_response=response,
                method=core.MethodsEnum.FALLBACK_SCSV_DISABLED,
            )
        )
    sock.close()

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _tlsv1_3_downgrade(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    if SSLVersionId.tlsv1_3 not in tls_versions:
        return tuple()

    en_intention = (
        "Perform a {v_name} request offering any cipher suite to check if\n"
        "the connection is accepted by the server, meaning that a downgrade\n"
        "from TLSv1.3 is possible"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo cualquier suite de\n"
        "cifrado para verificar si la conexión es aceptada por el servidor,\n"
        "lo cual significaria que TLSv1.3 puede ser degradado"
    )

    for v_id in tls_versions:
        if v_id in (SSLVersionId.tlsv1_2, SSLVersionId.tlsv1_3):
            continue

        v_name: str = ssl_id2ssl_name(v_id)
        ssl_settings = SSLSettings(
            context=ctx,
            tls_version=v_id,
            intention={
                core.LocalesEnum.EN: en_intention.format(v_name=v_name),
                core.LocalesEnum.ES: es_intention.format(v_name=v_name),
            },
        )

        ssl_vulnerabilities.append(
            _create_ssl_vuln(
                ssl_settings=ssl_settings,
                server_response=ctx.get_tls_response(v_id),
                method=core.MethodsEnum.TLSV1_3_DOWNGRADE,
                check_kwargs={"v_name": v_name},
            )
        )

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _heartbleed_possible(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: list[SSLSuiteInfo] = [
        SSLCipherSuite.ECDHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_256_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_256_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_3DES_EDE_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.SRP_SHA_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_AES_128_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_SEED_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_CAMELLIA_128_CBC_SHA.value,
        SSLCipherSuite.ECDHE_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDHE_ECDSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDH_RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.ECDH_ECDSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_SHA.value,
        SSLCipherSuite.RSA_WITH_RC4_128_MD5.value,
        SSLCipherSuite.DHE_RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.RSA_WITH_DES_CBC_SHA.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLSpecialSuite.EMPTY_RENEGOTIATION_INFO_SCSV.value,
    ]

    extensions: list[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    en_intention = (
        "Perform a {v_name} request offering any cipher suite and check if\n"
        "the server is vulnerable to a heartbleed attack"
    )

    es_intention = (
        "Realizar una petición {v_name} ofreciendo cualquier suite de\n"
        "cifrado y verificar si el servidor es vulnerable a un ataque\n"
        "heartbleed"
    )

    for v_id in tls_versions:
        intention: dict[core.LocalesEnum, str] = {
            core.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core.LocalesEnum.ES: (
                es_intention.format(
                    v_name=ssl_id2ssl_name(v_id),
                )
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(
            v_id=v_id,
            cipher_suites=suites,
            host=ctx.host,
            extensions=extensions,
        )
        sock.send(bytes(package))
        response: SSLServerResponse | None = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            package = get_malicious_heartbeat(v_id, n_payload=16384)
            sock.send(bytes(package))

            heartbeat_record = read_ssl_record(sock)

            if heartbeat_record is not None:
                heartbeat_type, _, _ = heartbeat_record

                if heartbeat_type == 24:
                    ssl_vulnerabilities.append(
                        _create_ssl_vuln(
                            ssl_settings=SSLSettings(
                                context=ctx,
                                tls_version=v_id,
                                intention=intention,
                            ),
                            server_response=response,
                            method=core.MethodsEnum.HEARTBLEED_POSSIBLE,
                            check_kwargs={"v_name": ssl_id2ssl_name(v_id)},
                        )
                    )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


def _freak_possible(ctx: SSLContext) -> core.Vulnerabilities:
    ssl_vulnerabilities: list[SSLVulnerability] = []
    tls_versions: tuple[SSLVersionId, ...] = ctx.get_supported_tls_versions()

    suites: list[SSLSuiteInfo] = [
        SSLSpecialSuite.RESERVED_SUITE_00_62.value,
        SSLSpecialSuite.RESERVED_SUITE_00_61.value,
        SSLSpecialSuite.RESERVED_SUITE_00_64.value,
        SSLSpecialSuite.RESERVED_SUITE_00_60.value,
        SSLCipherSuite.DHE_RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.DHE_DSS_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_DES40_CBC_SHA.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC2_CBC_40_MD5.value,
        SSLCipherSuite.RSA_EXPORT_WITH_RC4_40_MD5.value,
        SSLSpecialSuite.EMPTY_RENEGOTIATION_INFO_SCSV.value,
    ]

    extensions: list[int] = get_ec_point_formats_ext()
    extensions += get_elliptic_curves_ext()
    extensions += get_session_ticket_ext()
    extensions += get_heartbeat_ext()

    en_intention = (
        "Check if server is vulnerable to FREAK attack with {v_name}"
    )

    es_intention = (
        "Verificar si el servidor es vulnerable a ataques FREAK en {v_name}"
    )

    for v_id in tls_versions:
        intention: dict[core.LocalesEnum, str] = {
            core.LocalesEnum.EN: (
                en_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
            core.LocalesEnum.ES: (
                es_intention.format(v_name=ssl_id2ssl_name(v_id))
            ),
        }

        sock = tcp_connect(
            ctx.host,
            ctx.port,
            intention[core.LocalesEnum.EN],
        )

        if sock is None:
            break

        package = get_client_hello_package(
            v_id=v_id,
            cipher_suites=suites,
            host=ctx.host,
            extensions=extensions,
        )
        sock.send(bytes(package))
        response: SSLServerResponse | None = parse_server_response(sock)

        if response is not None and response.handshake is not None:
            ssl_vulnerabilities.append(
                _create_ssl_vuln(
                    ssl_settings=SSLSettings(
                        context=ctx,
                        tls_version=v_id,
                        key_exchange_names=["RSA"],
                        intention=intention,
                    ),
                    server_response=response,
                    method=core.MethodsEnum.FREAK_POSSIBLE,
                    check_kwargs={"v_name": ssl_id2ssl_name(v_id)},
                )
            )
        sock.close()

    return _create_core_vulns(ssl_vulnerabilities=ssl_vulnerabilities)


CHECKS: dict[
    core.FindingEnum,
    list[Callable[[SSLContext], core.Vulnerabilities]],
] = {
    core.FindingEnum.F052: [_weak_ciphers_allowed],
    core.FindingEnum.F094: [_cbc_enabled],
    core.FindingEnum.F133: [_pfs_disabled],
    core.FindingEnum.F016: [
        _sslv3_enabled,
        _tlsv1_enabled,
        _tlsv1_1_enabled,
        _tlsv1_2_or_higher_disabled,
        _fallback_scsv_disabled,
        _tlsv1_3_downgrade,
        _heartbleed_possible,
        _freak_possible,
    ],
}
