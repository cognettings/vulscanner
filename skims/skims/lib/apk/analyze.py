from .analyze_bytecodes import (
    CHECKS as APK_METHODS,
)
from .apk_utils import (
    APKCheckCtx,
    APKContext,
    get_apk_context,
    get_check_ctx as resolve_check_ctx,
)
from collections.abc import (
    Callable,
    Generator,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
import ctx
from model.core import (
    FindingEnum,
    Vulnerabilities,
    Vulnerability,
)
from more_itertools.more import (
    collapse,
)
from os import (
    cpu_count,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.fs import (
    resolve_paths,
)
from utils.function import (
    shield_blocking,
)
from utils.logs import (
    log_blocking,
)

CHECKS: tuple[
    tuple[
        Callable[[APKContext], APKCheckCtx],
        dict[
            FindingEnum,
            list[Callable[[APKCheckCtx], Vulnerabilities]],
        ],
    ],
    ...,
] = ((resolve_check_ctx, APK_METHODS),)


@shield_blocking(on_error_return=[])
def analyze_one(
    apk_ctx: APKContext,
) -> tuple[Vulnerability, ...]:
    return tuple(
        vulnerability
        for get_check_ctx, checks in CHECKS
        for finding, check_list in checks.items()
        if finding in ctx.SKIMS_CONFIG.checks and apk_ctx.apk_obj is not None
        for check in check_list
        for vulnerability in check(get_check_ctx(apk_ctx))
    )


def get_apk_contexts() -> Generator[APKContext, None, None]:
    ok_paths, nu_paths, nv_paths = resolve_paths(
        include=ctx.SKIMS_CONFIG.apk.include,
        exclude=ctx.SKIMS_CONFIG.apk.exclude,
    )

    all_paths = ok_paths + nu_paths + nv_paths
    log_blocking("info", "Files to be tested: %s", len(all_paths))
    for result in (get_apk_context(path) for path in all_paths):
        if result:
            yield result


def analyze(
    *,
    stores: dict[FindingEnum, EphemeralStore],
) -> None:
    if not any(
        finding in ctx.SKIMS_CONFIG.checks
        for _, checks in CHECKS
        for finding in checks
    ):
        return

    unique_apk_contexts: set[APKContext] = set(get_apk_contexts())
    vulnerabilities: tuple[Vulnerability, ...] = tuple(
        collapse(
            (analyze_one(x) for x in unique_apk_contexts),
            base_type=Vulnerability,
        )
    )
    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        list(
            worker.map(
                lambda x: stores[  # pylint: disable=unnecessary-lambda
                    x.finding
                ].store(x),
                vulnerabilities,
            )
        )
