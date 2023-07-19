from cli import (
    cli,
)
from collections.abc import (
    Callable,
    Iterable,
)
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import csv
import io
from itertools import (
    zip_longest,
)
import os
from typing import (
    Text,
)
from utils.logs import (
    configure,
)


def _default_snippet_filter(snippet: str) -> str:
    return snippet


def _format_csv(
    content: Iterable[Text],
    *,
    snippet_filter: Callable[[str], str],
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in csv.DictReader(content):
        row["snippet"] = snippet_filter(row["snippet"])
        result.append(row)
    result.sort(key=str)
    return result


def _get_suite_expected_results(suite: str, multifile: bool) -> str:
    paths = {
        True: f"skims/test/data/results/multifile/{suite}.csv",
        False: f"skims/test/data/results/{suite}.csv",
    }
    return paths[multifile]


def _get_suite_produced_results(suite: str, multifile: bool) -> str:
    paths = {
        True: f"skims/test/outputs/multifile/{suite}.csv",
        False: f"skims/test/outputs/{suite}.csv",
    }
    return paths[multifile]


def get_suite_config(suite: str) -> str:
    return f"skims/test/data/config/{suite}.yaml"


def create_config(
    finding: str,
    template: str,
) -> str:
    with open(template, "r", encoding="utf-8") as file:
        content = file.read()
        content = content.replace("{FINDING}", str(finding))
        content = content.replace("{FINDING_LOWER}", str(finding.lower()))
        return content


def skims(*args: str) -> tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    code: int = 0
    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            configure()
            cli.main(args=list(args), prog_name="skims")
        except SystemExit as exc:  # NOSONAR
            if isinstance(exc.code, int):
                code = exc.code
    try:
        return code, out_buffer.getvalue(), err_buffer.getvalue()
    finally:
        del out_buffer
        del err_buffer


def check_that_csv_results_match(
    suite: str,
    multifile: bool = False,
    *,
    snippet_filter: Callable[[str], str] = _default_snippet_filter,
) -> None:
    with open(
        _get_suite_produced_results(suite, multifile), encoding="utf-8"
    ) as produced:
        expected_path = os.path.join(
            os.environ["STATE"], _get_suite_expected_results(suite, multifile)
        )
        os.makedirs(os.path.dirname(expected_path), exist_ok=True)
        with open(expected_path, "w", encoding="utf-8") as expected:
            expected.write(produced.read())
            produced.seek(0)

        with open(
            _get_suite_expected_results(suite, multifile), encoding="utf-8"
        ) as expected:
            for producted_item, expected_item in zip_longest(
                _format_csv(produced, snippet_filter=snippet_filter),
                _format_csv(expected, snippet_filter=snippet_filter),
                fillvalue=None,
            ):
                assert producted_item == expected_item
