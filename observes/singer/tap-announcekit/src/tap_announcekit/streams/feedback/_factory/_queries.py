from dataclasses import (
    dataclass,
)
from purity.v1 import (
    Transform,
)
from returns.io import (
    IO,
)
from tap_announcekit.api.client import (
    Operation,
    Query,
    QueryFactory,
)
from tap_announcekit.api.gql_schema import (
    PageOfFeedback as RawFeedbackPage,
)
from tap_announcekit.objs.id_objs import (
    PostId,
    ProjectId,
)
from tap_announcekit.objs.page import (
    DataPage,
)
from tap_announcekit.objs.post import (
    Feedback,
)
from tap_announcekit.objs.post.feedback import (
    FeedbackObj,
)
from tap_announcekit.streams._query_utils import (
    select_fields,
    select_page_fields,
)
from typing import (
    Any,
    cast,
    Union,
)

_FeedbackId = Union[ProjectId, PostId]


@dataclass(frozen=True)
class FeedbackPageQuery:
    _to_obj: Transform[RawFeedbackPage, DataPage[FeedbackObj]]
    id_obj: _FeedbackId
    page: int

    @staticmethod
    def _attr_map(attr: str) -> str:
        mapping = {"comment": "feedback"}
        return mapping.get(attr, attr)

    def _fb_page(self, operation: Operation) -> Any:
        if isinstance(self.id_obj, PostId):
            return operation.feedbacks(
                project_id=self.id_obj.proj.id_str,
                post_id=self.id_obj.id_str,
                page=self.page,
            )
        return operation.feedbacks(
            project_id=self.id_obj.id_str, page=self.page
        )

    def _select_fields(self, operation: Operation) -> IO[None]:
        fb_page = self._fb_page(operation)
        items = fb_page.items()
        select_page_fields(fb_page)
        select_fields(
            items,
            frozenset(self._attr_map(x) for x in Feedback.__annotations__),
        )
        items.id()
        if isinstance(self.id_obj, ProjectId):
            items.post_id()
        return IO(None)

    @property
    def query(self) -> Query[DataPage[FeedbackObj]]:
        return QueryFactory.select(
            self._select_fields,
            Transform(
                lambda p: self._to_obj(
                    cast(RawFeedbackPage, p.feedbacks),
                )
            ),
        )
