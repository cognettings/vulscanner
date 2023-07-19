from .streams import (
    JobStreams,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from fa_purity import (
    Cmd,
    Maybe,
)
from fa_purity.stream.transform import (
    consume,
)
import logging
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.http_json_client import (
    HttpJsonClient,
)
from tap_gitlab.api.jobs import (
    Job,
    JobObj,
    JobsClient,
    JobsFilter,
    JobStatus,
)

LOG = logging.getLogger(__name__)
NOW = datetime.now(timezone.utc)


def clean_stuck_jobs(
    client: HttpJsonClient,
    project: ProjectId,
    start_page: int,
    threshold: timedelta,
    dry_run: bool,
) -> Cmd[None]:
    # threshold: how old a job should be for considering it stuck
    def is_stuck(job: Job) -> bool:
        diff = NOW - job.dates.created_at
        return diff > threshold

    status = frozenset(
        [JobStatus.created, JobStatus.pending, JobStatus.running]
    )
    _filter = JobsFilter(Maybe.from_value(status), True)
    job_client = JobsClient(client, project, Maybe.from_value(_filter))
    jobs_streamer = JobStreams(job_client)

    stuck_jobs = jobs_streamer.jobs(start_page, 100).filter(
        lambda j: is_stuck(j.obj)
    )

    def cancel_cmd(job: JobObj) -> Cmd[None]:
        diff = NOW - job.obj.dates.created_at
        if dry_run:
            return Cmd.from_cmd(
                lambda: LOG.info(
                    "%s will be cancelled. diff=%s", job.job_id, diff
                )
            )
        return job_client.cancel(job.job_id)

    return stuck_jobs.map(lambda j: cancel_cmd(j)).transform(
        lambda s: consume(s)
    )
