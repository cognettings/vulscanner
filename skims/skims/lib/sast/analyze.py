import ctx
from lib.path.analyze import (
    analyze as analyze_paths,
)
from lib.root.analyze import (
    analyze as analyze_root,
)
from lib.sast.types import (
    Paths,
)
from model.core import (
    FindingEnum,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.logs import (
    log_blocking,
)


def analyze(stores: dict[FindingEnum, EphemeralStore]) -> None:
    paths = Paths(ctx.SKIMS_CONFIG.sast.include, ctx.SKIMS_CONFIG.sast.exclude)
    log_blocking("info", "Files to be tested: %s", len(paths.get_all()))

    if ctx.SKIMS_CONFIG.sast.lib_path:
        analyze_paths(paths=paths, stores=stores)
    if ctx.SKIMS_CONFIG.sast.lib_root:
        paths.set_lang()
        analyze_root(paths=paths.ok_paths, stores=stores)
