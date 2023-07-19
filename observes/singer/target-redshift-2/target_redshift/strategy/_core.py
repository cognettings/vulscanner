from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from redshift_client.core.id_objs import (
    SchemaId,
)
from typing import (
    Callable,
)

LoadProcedure = Callable[[SchemaId], Cmd[None]]


@dataclass(frozen=True)
class LoadingStrategy:
    """
    Is a procedure that adds pre and post upload operations for
    the supplied `LoadProcedure`
    """

    _main: Callable[[LoadProcedure], Cmd[None]]

    def main(self, procedure: LoadProcedure) -> Cmd[None]:
        return self._main(procedure)
