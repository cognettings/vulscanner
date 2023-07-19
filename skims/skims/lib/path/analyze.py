from concurrent.futures.process import (
    ProcessPoolExecutor,
)
import ctx
from functools import (
    partial,
)
from lib.path import (
    f009,
    f015,
    f022,
    f037,
    f044,
    f052,
    f055,
    f058,
    f060,
    f065,
    f075,
    f079,
    f086,
    f097,
    f117,
    f135,
    f149,
    f152,
    f153,
    f176,
    f183,
    f239,
    f266,
    f325,
    f332,
    f346,
    f380,
    f403,
    f405,
    f418,
    f427,
)
from lib.sast.types import (
    Paths,
)
from model.core import (
    FindingEnum,
    SkimsConfig,
    Vulnerabilities,
    Vulnerability,
)
import os
from os.path import (
    split,
    splitext,
)
import reactivex
from reactivex import (
    operators as ops,
)
from schedulers.report import (
    send_vulnerability_to_sqs,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)
from utils.fs import (
    generate_file_raw_content_blocking,
    get_file_content_block,
)
from utils.logs import (
    log_blocking,
    log_exception_blocking,
)

# Constants
MEBIBYTE: int = 1048576
MAX_READ: int = 64 * MEBIBYTE

CHECKS: tuple[tuple[FindingEnum, Any], ...] = (
    (FindingEnum.F009, f009.analyze),
    (FindingEnum.F015, f015.analyze),
    (FindingEnum.F022, f022.analyze),
    (FindingEnum.F037, f037.analyze),
    (FindingEnum.F044, f044.analyze),
    (FindingEnum.F052, f052.analyze),
    (FindingEnum.F055, f055.analyze),
    (FindingEnum.F058, f058.analyze),
    (FindingEnum.F060, f060.analyze),
    (FindingEnum.F065, f065.analyze),
    (FindingEnum.F075, f075.analyze),
    (FindingEnum.F079, f079.analyze),
    (FindingEnum.F086, f086.analyze),
    (FindingEnum.F097, f097.analyze),
    (FindingEnum.F117, f117.analyze),
    (FindingEnum.F135, f135.analyze),
    (FindingEnum.F149, f149.analyze),
    (FindingEnum.F152, f152.analyze),
    (FindingEnum.F153, f153.analyze),
    (FindingEnum.F176, f176.analyze),
    (FindingEnum.F183, f183.analyze),
    (FindingEnum.F239, f239.analyze),
    (FindingEnum.F266, f266.analyze),
    (FindingEnum.F325, f325.analyze),
    (FindingEnum.F332, f332.analyze),
    (FindingEnum.F346, f346.analyze),
    (FindingEnum.F380, f380.analyze),
    (FindingEnum.F403, f403.analyze),
    (FindingEnum.F405, f405.analyze),
    (FindingEnum.F418, f418.analyze),
    (FindingEnum.F427, f427.analyze),
)


def analyze_one_path(  # noqa: MC0001
    *,
    index: int,
    path: str,
    finding_checks: set[FindingEnum],
    unique_nu_paths: set[str],
    unique_nv_paths: set[str],
    unique_paths_count: int,
    file_content: str,
) -> dict[FindingEnum, list[Vulnerabilities]]:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    """
    log_blocking(
        "info",
        "Analyzing path %s of %s: %s",
        index + 1,
        unique_paths_count,
        path,
    )

    def file_content_generator() -> str:
        return file_content

    file_raw_content_generator = generate_file_raw_content_blocking(
        path, size=MAX_READ
    )

    _, file_info = split(path)
    file_name, file_extension = splitext(file_info)
    file_extension = file_extension[1:]

    result: dict[FindingEnum, list[Vulnerabilities]] = {}

    for finding, analyzer in CHECKS:
        if finding not in finding_checks:
            continue

        if path in unique_nv_paths:
            if finding is not FindingEnum.F117:
                continue
        else:
            if finding in {
                FindingEnum.F117,
            }:
                continue

        result[finding] = analyzer(
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            finding=finding,
            path=path,
            raw_content_generator=file_raw_content_generator,
            unique_nu_paths=unique_nu_paths,
        )

    return result


def _analyze_one_path(  # noqa: MC0001
    *,
    config: SkimsConfig,
    index: int,
    path: str,
    checks: set[FindingEnum],
    unique_nu_paths: set[str],
    unique_nv_paths: set[str],
    unique_paths_count: int,
) -> dict[FindingEnum, list[Vulnerabilities]]:
    # Re-export config to gain visibility in child subprocesses
    ctx.SKIMS_CONFIG = config

    content = get_file_content_block(path)
    return analyze_one_path(
        index=index,
        path=path,
        finding_checks=checks,
        file_content=content,
        unique_nu_paths=unique_nu_paths,
        unique_nv_paths=unique_nv_paths,
        unique_paths_count=unique_paths_count,
    )


def _handle_result(
    stores: dict[FindingEnum, EphemeralStore],
    result: tuple[FindingEnum, Vulnerability],
) -> None:
    stores[result[0]].store(result[1])
    send_vulnerability_to_sqs(result[1])


def _handle_exception(
    exception: Exception, _observable: reactivex.Observable
) -> reactivex.Observable:
    log_exception_blocking("error", exception)
    return reactivex.of(None)


def analyze(
    *,
    paths: Paths,
    stores: dict[FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in ctx.SKIMS_CONFIG.checks for finding, _ in CHECKS):
        # No findings will be executed, early abort
        return

    all_paths = paths.get_all()
    unique_paths_count: int = len(all_paths)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        reactivex.of(*all_paths).pipe(
            ops.flat_map_indexed(
                lambda path, index: reactivex.from_future(  # type: ignore
                    executor.submit(  # type: ignore
                        _analyze_one_path,
                        config=ctx.SKIMS_CONFIG,
                        index=index,
                        path=path,
                        checks=ctx.SKIMS_CONFIG.checks,
                        unique_nu_paths=set(paths.nu_paths),
                        unique_nv_paths=set(paths.nv_paths),
                        unique_paths_count=unique_paths_count,
                    )
                ).pipe(ops.catch(_handle_exception))
            ),
            ops.filter(lambda x: x is not None),  # type: ignore
            ops.flat_map(
                lambda res: reactivex.of(  # type: ignore
                    *[
                        (finding, vuln)
                        for finding, vulns_list in res.items()  # type: ignore
                        for vulns in vulns_list
                        for vuln in vulns
                    ]
                )
            ),
        ).subscribe(
            on_next=partial(_handle_result, stores),
            on_error=lambda e: log_blocking("exception", e),  # type: ignore
        )
