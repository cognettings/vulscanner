from click.testing import (
    CliRunner,
)
from forces.cli import (
    main,
)
from forces.model import (
    StatusCode,
)
import os


def test_cli_invalid_config(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ("--token", test_token, "--strict", "--repo-name", "universes"),
    )
    assert result.exit_code == StatusCode.ERROR, result.exception


def test_cli_strict_no_breaking(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        ("--token", test_token, "--strict", "--repo-name", "universe"),
    )
    assert result.exit_code == StatusCode.BREAK_BUILD, result.exception


def test_cli_strict_breaking_low(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        (
            "--token",
            test_token,
            "--strict",
            "--repo-name",
            "universe",
            "--breaking",
            "2",
        ),
    )
    assert result.exit_code == StatusCode.BREAK_BUILD, result.exception


def test_cli_strict_breaking_high(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        (
            "--token",
            test_token,
            "--strict",
            "--repo-name",
            "universe",
            "--breaking",
            "10",
        ),
    )
    assert result.exit_code == StatusCode.SUCCESS, result.exception


def test_cli_lax(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ("--token", test_token, "--lax", "--repo-path", "../")
    )
    assert result.exit_code == StatusCode.SUCCESS, result.exception


def test_cli_invalid_group(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main, ("--token", test_token, "--lax", "--repo-path", "../")
    )
    assert result.exit_code == StatusCode.SUCCESS, result.exception


def test_cli_out_to_file(test_token: str) -> None:
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            main,
            (
                "--token",
                test_token,
                "--strict",
                "--output",
                "test.yml",
                "--repo-path",
                "../",
            ),
        )
        assert os.path.exists(f"{os.getcwd()}/test.yml"), result.exception


def test_cli_lax_feature_preview(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        (
            "--token",
            test_token,
            "--lax",
            "--repo-name",
            "universe",
            "--feature-preview",
        ),
    )
    assert result.exit_code == StatusCode.SUCCESS, result.exception


def test_cli_strict_feature_preview(test_token: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        (
            "--token",
            test_token,
            "--strict",
            "--repo-name",
            "universe",
            "--feature-preview",
        ),
    )
    assert result.exit_code == StatusCode.BREAK_BUILD, result.exception
