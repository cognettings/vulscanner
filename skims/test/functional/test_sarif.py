from ..utils import (
    skims,
)
import os
import pytest
from pytest_mock import (
    MockerFixture,
)
import yaml  # type: ignore


def _format_sarif_res(
    content: dict,
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for report in content:
        report_summary = {
            "vuln_id": report["guid"],
            "vuln_where": report["locations"][0]["physicalLocation"][
                "artifactLocation"
            ]["uri"],
            "vuln_specific": report["locations"][0]["physicalLocation"][
                "region"
            ]["startLine"],
        }
        results.append(report_summary)
    results.sort(key=lambda report: report["vuln_id"])
    return results


def check_that_sarif_results_match() -> None:
    with open("skims/test/outputs/report.sarif", encoding="utf-8") as produced:
        expected_path = os.path.join(
            os.environ["STATE"], "skims/test/data/sarif/report.sarif"
        )
        os.makedirs(os.path.dirname(expected_path), exist_ok=True)
        with open(expected_path, "w", encoding="utf-8") as expected:
            expected.write(produced.read())
            produced.seek(0)

        with open(
            "skims/test/data/sarif/report.sarif", encoding="utf-8"
        ) as expected:
            for produced_item, expected_item in zip(
                _format_sarif_res(
                    yaml.safe_load(produced)["runs"][0]["results"]
                ),
                _format_sarif_res(
                    yaml.safe_load(expected)["runs"][0]["results"]
                ),
            ):
                assert (
                    produced_item["vuln_id"] == expected_item["vuln_id"]
                ), "Vuln ID changed, make sure this change is intended"
                assert (
                    produced_item["vuln_where"] == expected_item["vuln_where"]
                ), "Vuln location changed, make sure this change is intended"
                assert (
                    produced_item["vuln_specific"]
                    == expected_item["vuln_specific"]
                ), "Vuln specific changed, make sure this change is intended"


def run_skims_for_sarif(mocker: MockerFixture) -> None:
    path = "skims/test/data/sarif/config.yaml"
    with mocker.patch(
        "core.result.get_repo_branch",
        return_value="trunk",
    ):
        code, stdout, stderr = skims("scan", path)
    assert code == 0, stdout
    assert "[INFO] Startup work dir is:" in stdout
    assert not stderr, stderr
    check_that_sarif_results_match()


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("sarif_report")
def test_sarif_report(mocker: MockerFixture) -> None:
    run_skims_for_sarif(mocker)
