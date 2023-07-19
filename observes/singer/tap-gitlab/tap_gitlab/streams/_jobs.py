from ._utils import (
    GenericStream,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Stream,
)
from tap_gitlab.api.core.ids import (
    PipelineId,
)
from tap_gitlab.api.jobs import (
    JobId,
    JobObj,
    JobsClient,
)


@dataclass(frozen=True)
class JobStreams:
    _client: JobsClient

    def jobs(self, start_page: int, per_page: int) -> Stream[JobObj]:
        return GenericStream(start_page, per_page).generic_page_stream(
            lambda p: self._client.jobs_page(p), GenericStream.is_empty
        )

    def job_ids(self, start_page: int, per_page: int) -> Stream[JobId]:
        return GenericStream(start_page, per_page).generic_page_stream(
            lambda p: self._client.jobs_ids_page(p), GenericStream.is_empty
        )

    def pipeline_jobs(
        self, pipeline: PipelineId, start_page: int, per_page: int
    ) -> Stream[JobObj]:
        return GenericStream(start_page, per_page).generic_page_stream(
            lambda p: self._client.pipeline_jobs_page(pipeline, p),
            GenericStream.is_empty,
        )
