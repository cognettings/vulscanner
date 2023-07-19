from __future__ import (
    annotations,
)

import csv
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.json.primitive.core import (
    Primitive,
)
from typing import (
    Any,
    IO,
)


@dataclass(frozen=True)  # type: ignore[misc]
class _CsvWriter:  # type: ignore[misc]
    """csv writer wrapper"""

    writer: Any  # type: ignore[misc]


@dataclass(frozen=True)
class CsvWriter:
    """csv writer wrapper"""

    _inner: _CsvWriter

    @staticmethod
    def new(file: IO[str]) -> Cmd[CsvWriter]:
        def _action() -> CsvWriter:
            writer = csv.writer(
                file,
                delimiter=",",
                quotechar='"',
                doublequote=True,
                escapechar="\\",
                quoting=csv.QUOTE_MINIMAL,
            )
            return CsvWriter(_CsvWriter(writer))

        return Cmd.from_cmd(_action)

    def write_row(self, row: FrozenList[Primitive]) -> Cmd[None]:
        def _action() -> None:
            self._inner.writer.writerow(row)  # type: ignore[misc]

        return Cmd.from_cmd(_action)

    def write_rows(self, row: FrozenList[FrozenList[Primitive]]) -> Cmd[None]:
        def _action() -> None:
            self._inner.writer.writerows(row)  # type: ignore[misc]

        return Cmd.from_cmd(_action)
