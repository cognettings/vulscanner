from ..utils import (
    check_that_csv_results_match,
    get_suite_config,
    skims,
)
from collections.abc import (
    Callable,
)
import pytest


def _default_snippet_filter(snippet: str) -> str:
    return snippet


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_apk")
def test_lib_apk() -> None:
    _run_no_group("lib_apk")


@pytest.mark.flaky(reruns=3)  # The outcome depends on third party servers
@pytest.mark.skims_test_group("lib_http")
@pytest.mark.usefixtures("test_mocks_http")
def test_lib_http() -> None:
    def snippet_filter(snippet: str | None) -> str:
        if not snippet:
            snippet = ""
        return "\n".join(
            line
            for line in snippet.splitlines()
            if snippet and "< Date:" not in line
        )

    _run_no_group("lib_http", snippet_filter=snippet_filter)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_http_2")
def test_lib_http_2() -> None:
    _run_no_group("lib_http_2")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_ssl")
@pytest.mark.usefixtures("test_mocks_ssl_safe", "test_mocks_ssl_unsafe")
def test_lib_ssl() -> None:
    _run_no_group("lib_ssl")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_cmdi")
def test_benchmark_cmdi() -> None:
    _run_no_group("benchmark_owasp_cmdi")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_crypto")
def test_benchmark_crypto() -> None:
    _run_no_group("benchmark_owasp_crypto")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_hash")
def test_benchmark_hash() -> None:
    _run_no_group("benchmark_owasp_hash")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_ldapi")
def test_benchmark_ldapi() -> None:
    _run_no_group("benchmark_owasp_ldapi")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_pathtraver")
def test_benchmark_pathtraver() -> None:
    _run_no_group("benchmark_owasp_pathtraver")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_securecookie")
def test_benchmark_securecookie() -> None:
    _run_no_group("benchmark_owasp_securecookie")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_sqli")
def test_benchmark_sqli() -> None:
    _run_no_group("benchmark_owasp_sqli")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_trustbound")
def test_benchmark_trustbound() -> None:
    _run_no_group("benchmark_owasp_trustbound")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_weakrand")
def test_benchmark_weakrand() -> None:
    _run_no_group("benchmark_owasp_weakrand")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_xpathi")
def test_benchmark_xpathi() -> None:
    _run_no_group("benchmark_owasp_xpathi")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_xss")
def test_benchmark_xss() -> None:
    _run_no_group("benchmark_owasp_xss")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("instance_references")
def test_instance_reference() -> None:
    _run_no_group("instance_references")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("vulnerableapp")
def test_vulnerableapp() -> None:
    _run_no_group("vulnerableapp")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("vulnerable_js_app")
def test_vulnerable_js_app() -> None:
    _run_no_group("vulnerable_js_app")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f001")
def test_nist_c_sharp_f001() -> None:
    _run_no_group("nist_c_sharp_f001")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f004")
def test_nist_c_sharp_f004() -> None:
    _run_no_group("nist_c_sharp_f004")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f008")
def test_nist_c_sharp_f008() -> None:
    _run_no_group("nist_c_sharp_f008")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f021")
def test_nist_c_sharp_f021() -> None:
    _run_no_group("nist_c_sharp_f021")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f052")
def test_nist_c_sharp_f052() -> None:
    _run_no_group("nist_c_sharp_f052")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f063")
def test_nist_c_sharp_f063() -> None:
    _run_no_group("nist_c_sharp_f063")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f107")
def test_nist_c_sharp_f107() -> None:
    _run_no_group("nist_c_sharp_f107")


def _run_no_group(
    suite: str,
    *,
    snippet_filter: Callable[[str], str] = _default_snippet_filter,
) -> None:
    code, stdout, stderr = skims("scan", get_suite_config(suite))
    assert code == 0, stdout
    assert "[INFO] Startup work dir is:" in stdout
    assert "[INFO] An output file has been written:" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite, snippet_filter=snippet_filter)
