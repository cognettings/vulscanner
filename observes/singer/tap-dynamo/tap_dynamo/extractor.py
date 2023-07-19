from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    FrozenList,
    Stream,
)
from fa_purity.cmd import (
    Cmd,
    CmdUnwrapper,
    unsafe_unwrap,
)
from fa_purity.json.factory import (
    load,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from fa_purity.pure_iter.transform import (
    consume as piter_consume,
)
from fa_purity.stream.factory import (
    unsafe_from_cmd,
)
from fa_purity.stream.transform import (
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
)
import os
import simplejson
import sys
from tap_dynamo import (
    _utils,
)
from tap_dynamo.client import (
    Client,
    ScanArgs,
)
import tempfile
from threading import (
    Lock,
)
from typing import (
    Any,
    Callable,
    Dict,
    IO as FILE,
    Iterable,
    Optional,
    TypeVar,
)

_K = TypeVar("_K")
_P = TypeVar("_P")


@dataclass(frozen=True)
class TableSegment:
    table_name: str
    segment: int
    total_segments: int


@dataclass(frozen=True)
class PageData:
    t_segment: TableSegment
    file: FILE[str]
    exclusive_start_key: Optional[FrozenDict[str, Any]]

    def destroy(self) -> Cmd[None]:
        return Cmd.from_cmd(lambda: os.remove(self.file.name))


@dataclass(frozen=True)
class ScanResponse:
    t_segment: TableSegment
    response: FrozenDict[str, Any]


def paginate_table(
    client: Client,
    table_segment: TableSegment,
    ex_start_key: Optional[Any],
) -> Cmd[ScanResponse]:
    table = client.table(table_segment.table_name)
    scan_args = ScanArgs(
        1000,
        False,
        table_segment.segment,
        table_segment.total_segments,
        ex_start_key,
    )
    result = table.scan(scan_args)
    return result.map(
        lambda r: ScanResponse(t_segment=table_segment, response=r)
    )


class SetEncoder(simplejson.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return list(o)
        return simplejson.JSONEncoder.default(self, o)


def response_to_page(scan_response: ScanResponse) -> Optional[PageData]:
    response = dict(scan_response.response)
    if response.get("Count") == 0:
        return None

    last_key: Optional[Dict[str, Any]] = response.get("LastEvaluatedKey", None)
    data = simplejson.dumps(response, cls=SetEncoder)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as file:
        file.write(data)
        if last_key:
            return PageData(
                t_segment=scan_response.t_segment,
                file=file,
                exclusive_start_key=FrozenDict(last_key),
            )
        return PageData(
            t_segment=scan_response.t_segment,
            file=file,
            exclusive_start_key=None,
        )


def extract_until_end(
    getter: Callable[[Optional[_K]], Cmd[Optional[_P]]],
    extract_next: Callable[[_P], Optional[_K]],
) -> Stream[_P]:
    def _inner() -> Iterable[_P]:
        last_key: Optional[_K] = None
        end_reached: bool = False
        while not end_reached:
            result: Optional[_P] = unsafe_unwrap(getter(last_key))
            if not result:
                end_reached = True
                continue

            last_key = extract_next(result)
            if not last_key:
                end_reached = True
            yield result

    return unsafe_from_cmd(Cmd.from_cmd(_inner))


def extract_segment(
    db_client: Client, segment: TableSegment
) -> Stream[PageData]:
    def getter(
        last_key: Optional[FrozenDict[str, Any]]
    ) -> Cmd[Optional[PageData]]:
        response = paginate_table(db_client, segment, last_key)
        return response.map(response_to_page)

    return extract_until_end(getter, lambda p: p.exclusive_start_key)


def to_singer(page: PageData) -> FrozenList[SingerRecord]:
    with open(page.file.name, encoding="utf-8") as file:
        data = load(file).unwrap()
        return tuple(
            SingerRecord(
                page.t_segment.table_name,
                Unfolder(item).to_json().unwrap(),
                None,
            )
            for item in Unfolder(data["Items"]).to_list().unwrap()
        )


def _emit_page(page: PageData) -> Cmd[None]:
    return (
        from_flist(to_singer(page))
        .map(lambda i: emitter.emit(sys.stdout, i))
        .transform(piter_consume)
    ) + page.destroy()


def _emit_pages(lock: Lock, pages: Stream[PageData]) -> Cmd[None]:
    def _action(unwrapper: CmdUnwrapper) -> None:
        cmds = unwrapper.act(pages.map(_emit_page).unsafe_to_iter())
        for c in cmds:
            lock.acquire()
            try:
                unwrapper.act(c)
            finally:
                lock.release()

    return Cmd.new_cmd(_action)


def _process_streams_chunk(streams: FrozenList[Stream[PageData]]) -> Cmd[None]:
    lock = Lock()
    return _utils.threads_map(
        from_flist(streams).map(lambda p: _emit_pages(lock, p)).to_list()
    ).map(lambda _: None)


def stream_table(
    db_client: Client, table_name: str, segments: int, max_concurrency: int
) -> Cmd[None]:
    items = (
        from_range(range(segments)).map(
            lambda i: extract_segment(
                db_client, TableSegment(table_name, i, segments)
            )
        )
    ).chunked(max_concurrency)
    return piter_consume(items.map(_process_streams_chunk))


def stream_tables(
    client: Client,
    tables: FrozenList[str],
    segmentation: int,
    max_concurrency: int,
) -> Cmd[None]:
    pages = from_flist(tables).map(
        lambda t: stream_table(client, t, segmentation, max_concurrency)
    )
    return piter_consume(pages)


def stream_segment(db_client: Client, segment: TableSegment) -> Cmd[None]:
    return (
        extract_segment(db_client, segment)
        .map(to_singer)
        .map(lambda x: from_flist(x))
        .map(lambda s: s.map(lambda r: emitter.emit(sys.stdout, r)))
        .map(piter_consume)
        .transform(lambda x: consume(x))
    )
