from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    PureIter,
    Result,
    ResultE,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
import sys
from tap_gitlab._utils import (
    AppBug,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.core.job import (
    JobStatus,
)
from tap_gitlab.api.core.pipeline import (
    PipelineStatus,
)
from tap_gitlab.api.http_json_client import (
    Credentials,
    HttpJsonClient,
)
from tap_gitlab.api.issues import (
    IssueClient,
)
from tap_gitlab.api.members import (
    MembersClient,
)
from tap_gitlab.emitter import (
    MrsEmitter,
    PipeJobsEmitter,
    StatefullStreams,
    StatelessEmitter,
    StatelessStreams,
    SupportedStreams,
)
from tap_gitlab.state import (
    EtlState,
    PipeJobsStreamKey,
)
from tap_gitlab.state.getter import (
    S3URI,
    StateGetter,
)

LOG = logging.getLogger(__name__)


def get_state(state_uri: str) -> Cmd[ResultE[EtlState]]:
    _uri = S3URI.from_uri(state_uri)
    return (
        _uri.map(lambda uri: StateGetter.new().bind(lambda g: g.get(uri)))
        .alt(lambda e: Cmd.from_cmd(lambda: Result.failure(e, EtlState)))
        .to_union()
    )


_terminated_jobs_status = frozenset(
    [
        JobStatus.failed,
        JobStatus.success,
        JobStatus.canceled,
        JobStatus.skipped,
        JobStatus.manual,
    ]
)


def _stateful_router(
    client: HttpJsonClient,
    stream: StatefullStreams,
    project: ProjectId,
    max_pages: int,
    state: EtlState,
) -> Cmd[EtlState]:
    def _pipe_jobs(status: PipelineStatus) -> Cmd[EtlState]:
        return PipeJobsEmitter(
            sys.stdout,
            project,
            max_pages,
            PipeJobsStreamKey(status, _terminated_jobs_status),
            client,
        ).emit(state)

    if stream is StatefullStreams.MRS_CLOSED:
        return MrsEmitter(
            sys.stdout, project, max_pages
        ).closed_stream_emitter(client, state)
    if stream is StatefullStreams.MRS_MERGED:
        return MrsEmitter(
            sys.stdout, project, max_pages
        ).merged_stream_emitter(client, state)
    if stream is StatefullStreams.PIPE_JOBS_CANCELED:
        return _pipe_jobs(PipelineStatus.canceled)
    if stream is StatefullStreams.PIPE_JOBS_FAILED:
        return _pipe_jobs(PipelineStatus.failed)
    if stream is StatefullStreams.PIPE_JOBS_MANUAL:
        return _pipe_jobs(PipelineStatus.manual)
    if stream is StatefullStreams.PIPE_JOBS_SKIPPED:
        return _pipe_jobs(PipelineStatus.skipped)
    if stream is StatefullStreams.PIPE_JOBS_SUCCESS:
        return _pipe_jobs(PipelineStatus.success)


def _stateless_router(
    client: HttpJsonClient,
    stream: StatelessStreams,
    project: ProjectId,
    max_pages: int,
) -> Cmd[None]:
    if stream is StatelessStreams.ISSUES:
        return StatelessEmitter(sys.stdout, project, max_pages).issues(
            IssueClient(client, None)
        )
    if stream is StatelessStreams.MEMBERS:
        return StatelessEmitter(sys.stdout, project, max_pages).members(
            MembersClient(client)
        )


def cli_handler(
    api_key: str,
    project: str,
    streams: FrozenList[str],
    state_uri: Maybe[str],
    max_pages: int,
) -> Cmd[None]:
    _streams = from_flist(
        tuple(
            SupportedStreams.from_raw(s.upper()).unwrap().classify()
            for s in streams
        )
    )
    _stateful = _streams.filter(
        lambda u: u.map(lambda _: True, lambda _: False)
    ).map(
        lambda u: u.map(
            lambda x: x,
            lambda v: raise_exception(
                AppBug(
                    ValueError(f"Unexpected `StatelessStreams` value i.e. {v}")
                )
            ),
        )
    )
    _stateless = _streams.filter(
        lambda u: u.map(lambda _: False, lambda _: True)
    ).map(
        lambda u: u.map(
            lambda v: raise_exception(
                AppBug(
                    ValueError("Unexpected `StatefullStreams` value i.e. {v}")
                )
            ),
            lambda x: x,
        )
    )
    _project = ProjectId.from_name(project)
    client = HttpJsonClient.new(Credentials(api_key))

    _stateless_emissions = _stateless.map(
        lambda sl: _stateless_router(client, sl, _project, max_pages)
    ).transform(consume)

    def _stateful_emissions(streams: PureIter[StatefullStreams]) -> Cmd[None]:
        return (
            streams.reduce(
                lambda prev, sf: Maybe.from_value(
                    prev.or_else_call(
                        lambda: raise_exception(AppBug(ValueError("prev must exists!")))  # type: ignore[misc]
                    ).bind(  # if `state_uri` prev must exist
                        lambda r: Cmd.from_cmd(
                            lambda: LOG.info(
                                "Starting stateful emission: %s", sf
                            )
                        )
                        + _stateful_router(client, sf, _project, max_pages, r)
                    )
                ),
                state_uri.map(get_state).map(
                    lambda c: c.map(
                        lambda r: r.unwrap()  # if `state_uri` then decode must succeed
                    )
                ),
            )
            .map(lambda c: c.map(lambda _: None))
            .value_or(Cmd.from_cmd(lambda: None))
        )

    return _stateless_emissions + _stateful_emissions(_stateful)
