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
    PipelineRelativeId,
)
from tap_gitlab.api.pipelines import (
    PipelineClient,
)
from typing import (
    Tuple,
)


@dataclass(frozen=True)
class PipelineStreams:
    _client: PipelineClient

    def pipeline_id_stream(
        self, start_page: int, per_page: int
    ) -> Stream[Tuple[PipelineId, PipelineRelativeId]]:
        return GenericStream(start_page, per_page).generic_page_stream(
            lambda p: self._client.pipelines_ids_page(p),
            GenericStream.is_empty,
        )
