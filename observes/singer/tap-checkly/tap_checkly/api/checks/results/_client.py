from .time_range import (
    date_ranges_dsc,
    DateRange,
)
from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    PureIter,
    Stream,
)
from fa_purity.json.factory import (
    from_prim_dict,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_empty,
    until_none,
)
from tap_checkly.api._raw import (
    RawClient,
)
from tap_checkly.api.checks.results import (
    _decode,
)
from tap_checkly.objs import (
    CheckId,
    CheckResultObj,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class CheckResultClient:
    _client: RawClient
    _check: CheckId
    _per_page: int
    _from_date: datetime
    _to_date: datetime

    def _list_per_date_range(
        self,
        page: int,
        date_range: DateRange,
    ) -> Cmd[FrozenList[CheckResultObj]]:
        return self._client.get_list(
            "/v1/check-results/" + self._check.id_str,
            from_prim_dict(
                {
                    "limit": self._per_page,
                    "page": page,
                    "from": str(int(datetime.timestamp(date_range.from_date))),
                    "to": str(int(datetime.timestamp(date_range.to_date))),
                }
            ),
        ).map(
            lambda l: all_ok(
                from_flist(l)
                .map(lambda i: _decode.from_raw_obj(self._check, i))
                .to_list()
            ).unwrap()
        )

    def _date_ranges(self) -> PureIter[DateRange]:
        return date_ranges_dsc(self._from_date, self._to_date)

    def _list_all(
        self,
        dr: DateRange,
        list_cmd: Callable[[int, DateRange], Cmd[FrozenList[_T]]],
    ) -> Cmd[Maybe[Stream[_T]]]:
        first = list_cmd(1, dr)
        return first.map(
            lambda i: Maybe.from_optional(i if bool(i) else None).map(
                lambda f: infinite_range(1, 1)
                .map(
                    lambda p: list_cmd(p, dr)
                    if p > 1
                    else Cmd.from_cmd(lambda: f)
                )
                .transform(lambda x: from_piter(x))
                .map(lambda i: i if bool(i) else None)
                .transform(lambda x: until_none(x))
                .map(lambda x: from_flist(x))
                .transform(lambda x: chain(x))
            )
        )

    def list_all(self) -> Stream[CheckResultObj]:
        return (
            self._date_ranges()
            .map(lambda d: self._list_all(d, self._list_per_date_range))
            .transform(lambda x: from_piter(x))
            .transform(lambda x: until_empty(x))
            .bind(lambda s: s)
        )
