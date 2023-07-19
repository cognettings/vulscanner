from datetime import (
    datetime,
    timezone,
)
from fa_purity.frozen import (
    freeze,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.intervals import (
    ChainedOpenLeft,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    MIN,
)
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from tap_gitlab.state._objs import (
    EtlState,
    MrStateMap,
    MrStreamState,
)
from tap_gitlab.streams import (
    default_mr_streams,
)

NOW = datetime.now(timezone.utc)


def default_mr_state() -> MrStreamState:
    return MrStreamState(
        FragmentedProgressInterval.new(
            ChainedOpenLeft.new(
                IntervalFactory.datetime_default().greater, (MIN(), NOW)
            ).unwrap(),
            (False,),
        ).unwrap()
    )


def default_etl_state(
    project: ProjectId,
) -> EtlState:
    mr_streams = default_mr_streams(project)
    mrs_map = MrStateMap({stream: default_mr_state() for stream in mr_streams})
    return EtlState(freeze({}), mrs_map)
