from ..utils import (
    check_that_csv_results_match,
    create_config,
    skims,
)
import os
import pytest
import tempfile


def run_finding(finding: str) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, f"{finding}.yaml")
        with open(path, "w", encoding="utf-8") as tmpfile:
            template = "skims/test/data/config/template_multifile.yaml"
            tmpfile.write(create_config(finding, template))

        code, stdout, stderr = skims("scan", path)

        assert code == 0, stdout
        assert "[INFO] Startup work dir is:" in stdout
        assert "[INFO] An output file has been written:" in stdout
        assert not stderr, stderr
        check_that_csv_results_match(finding, multifile=True)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("multifile")
def test_multifile() -> None:
    run_finding("F052")
