from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Result,
    ResultE,
)


class InvalidPage(Exception):
    pass


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class Page:
    private: _Private = field(repr=False, hash=False, compare=False)
    page_num: int
    per_page: int

    @staticmethod
    def new_page(page_num: int, per_page: int) -> ResultE[Page]:
        if page_num > 0 and per_page in range(1, 101):
            pag = Page(_Private(), page_num, per_page)
            return Result.success(pag)
        return Result.failure(Exception(InvalidPage()))
