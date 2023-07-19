from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    PureIter,
)
from fa_purity.pure_iter.transform import (
    consume as piter_consume,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerSchema,
)
from tap_gitlab.api.core.ids import (
    ProjectId,
)
from tap_gitlab.api.issues import (
    IssueClient,
)
from tap_gitlab.api.members import (
    MembersClient,
)
from tap_gitlab.singer.issues import (
    records as issue_record,
    schemas as issue_schema,
)
from tap_gitlab.singer.members import (
    records as members_record,
    schemas as members_schema,
)
from typing import (
    IO,
)


@dataclass(frozen=True)
class StatelessEmitter:
    _target: IO[str]
    _project: ProjectId
    _page_limit: int

    def _emit_schemas(self, schemas: PureIter[SingerSchema]) -> Cmd[None]:
        return schemas.map(lambda s: emitter.emit(self._target, s)).transform(
            lambda x: piter_consume(x)
        )

    def issues(self, client: IssueClient) -> Cmd[None]:
        return self._emit_schemas(issue_schema.all_schemas()) + (
            client.project_issues(self._project)
            .map(issue_record.issue_records)
            .transform(lambda x: chain(x))
            .map(lambda s: emitter.emit(self._target, s))
            .transform(lambda x: consume(x))
        )

    def members(self, client: MembersClient) -> Cmd[None]:
        return self._emit_schemas(members_schema.all_schemas()) + (
            client.project_members(self._project)
            .map(lambda x: members_record.member_records(self._project, x))
            .transform(lambda x: chain(x))
            .map(lambda s: emitter.emit(self._target, s))
            .transform(lambda x: consume(x))
        )
