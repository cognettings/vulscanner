from concurrent.futures.process import (
    ProcessPoolExecutor,
)
import ctx
from functools import (
    partial,
)
from lib.sast.types import (
    Paths,
)
from lib.sca import (
    f011,
    f120,
    f393,
)
from model.core import (
    FindingEnum,
    SkimsConfig,
    Vulnerabilities,
    Vulnerability,
)
from model.graph import (
    GraphShardMetadataLanguage,
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
    (FindingEnum.F011, f011.analyze),
    (FindingEnum.F120, f120.analyze),
    (FindingEnum.F393, f393.analyze),
)


def analyze_one_path(  # noqa: MC0001
    *,
    index: int,
    path: str,
    finding_checks: set[FindingEnum],
    unique_nu_paths: set[str],
    unique_paths_count: int,
    file_content: str,
) -> dict[FindingEnum, list[Vulnerabilities]]:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    """
    log_blocking(
        "info",
        "(sca) analyzing path %s of %s: %s",
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
    stores: dict[FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in ctx.SKIMS_CONFIG.checks for finding, _ in CHECKS):
        # No findings will be executed, early abort
        return

    paths = Paths(ctx.SKIMS_CONFIG.sca.include, ctx.SKIMS_CONFIG.sca.exclude)
    paths.set_lang()
    all_paths = (
        paths.paths_by_lang[GraphShardMetadataLanguage.NOT_SUPPORTED]
        + paths.paths_by_lang[GraphShardMetadataLanguage.JSON]
        + paths.paths_by_lang[GraphShardMetadataLanguage.YAML]
    )
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
