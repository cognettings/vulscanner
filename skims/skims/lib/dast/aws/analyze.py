from aioextensions import (
    collect,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
import ctx
from lib.dast.aws import (
    f005,
    f016,
    f024,
    f031,
    f070,
    f073,
    f081,
    f099,
    f101,
    f109,
    f165,
    f177,
    f200,
    f203,
    f246,
    f250,
    f256,
    f257,
    f258,
    f259,
    f277,
    f281,
    f325,
    f333,
    f335,
    f363,
    f372,
    f394,
    f396,
    f400,
    f406,
    f407,
    f411,
    f433,
)
from model import (
    core,
)
from model.core import (
    AwsCredentials,
    Vulnerability,
)
from more_itertools import (
    collapse,
)
from os import (
    cpu_count,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)

CHECKS: tuple[tuple[core.FindingEnum, Any], ...] = (
    (core.FindingEnum.F005, [*f005.CHECKS]),
    (core.FindingEnum.F016, [*f016.CHECKS]),
    (core.FindingEnum.F024, [*f024.CHECKS]),
    (core.FindingEnum.F031, [*f031.CHECKS]),
    (core.FindingEnum.F070, [*f070.CHECKS]),
    (core.FindingEnum.F073, [*f073.CHECKS]),
    (core.FindingEnum.F081, [*f081.CHECKS]),
    (core.FindingEnum.F099, [*f099.CHECKS]),
    (core.FindingEnum.F101, [*f101.CHECKS]),
    (core.FindingEnum.F109, [*f109.CHECKS]),
    (core.FindingEnum.F165, [*f165.CHECKS]),
    (core.FindingEnum.F177, [*f177.CHECKS]),
    (core.FindingEnum.F200, [*f200.CHECKS]),
    (core.FindingEnum.F203, [*f203.CHECKS]),
    (core.FindingEnum.F246, [*f246.CHECKS]),
    (core.FindingEnum.F250, [*f250.CHECKS]),
    (core.FindingEnum.F256, [*f256.CHECKS]),
    (core.FindingEnum.F257, [*f257.CHECKS]),
    (core.FindingEnum.F258, [*f258.CHECKS]),
    (core.FindingEnum.F259, [*f259.CHECKS]),
    (core.FindingEnum.F277, [*f277.CHECKS]),
    (core.FindingEnum.F281, [*f281.CHECKS]),
    (core.FindingEnum.F325, [*f325.CHECKS]),
    (core.FindingEnum.F333, [*f333.CHECKS]),
    (core.FindingEnum.F335, [*f335.CHECKS]),
    (core.FindingEnum.F372, [*f372.CHECKS]),
    (core.FindingEnum.F363, [*f363.CHECKS]),
    (core.FindingEnum.F394, [*f394.CHECKS]),
    (core.FindingEnum.F396, [*f396.CHECKS]),
    (core.FindingEnum.F406, [*f406.CHECKS]),
    (core.FindingEnum.F400, [*f400.CHECKS]),
    (core.FindingEnum.F407, [*f407.CHECKS]),
    (core.FindingEnum.F411, [*f411.CHECKS]),
    (core.FindingEnum.F433, [*f433.CHECKS]),
)


async def analyze(
    *,
    credentials: AwsCredentials,
    stores: dict[core.FindingEnum, EphemeralStore],
) -> None:
    vulnerabilities: list[Vulnerability] = list(
        collapse(
            await collect(
                [
                    check(credentials)
                    for finding, checks in CHECKS
                    for check in checks
                    if finding in ctx.SKIMS_CONFIG.checks
                ]
            ),
            base_type=Vulnerability,
        )
    )
    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        worker.map(
            lambda x: stores[  # pylint: disable=unnecessary-lambda
                x.finding
            ].store(x),
            vulnerabilities,
        )
