import pytest
from test.utils import (
    get_suite_config,
    skims,
)


@pytest.mark.skims_test_group("unittesting")
def test_help() -> None:
    code, stdout, stderr = skims("--help")
    assert code == 0
    assert "Usage:" in stdout
    assert not stderr


@pytest.mark.skims_test_group("unittesting")
def test_non_existent_config() -> None:
    code, stdout, stderr = skims("scan", "#")
    assert code == 2
    assert not stdout, stdout
    assert "File '#' does not exist." in stderr, stderr


@pytest.mark.skims_test_group("unittesting")
def test_config_with_extra_parameters() -> None:
    suite: str = "bad_extra_things"
    code, stdout, stderr = skims("scan", get_suite_config(suite))
    assert code == 1
    assert "Some keys were not recognized: unrecognized_key" in stdout, stdout
    assert not stderr, stderr


@pytest.mark.skims_test_group("unittesting")
def test_strict_execution() -> None:
    suite: str = "strict_execution"
    code, _, stderr = skims("--strict", "scan", get_suite_config(suite))
    assert code == 1
    assert not stderr, stderr
