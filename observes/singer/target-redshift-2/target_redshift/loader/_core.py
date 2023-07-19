from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
)
from redshift_client.core.id_objs import (
    SchemaId,
)
from target_redshift.grouper import (
    PackagedSinger,
)
from typing import (
    Callable,
)


@dataclass(frozen=True)
class SingerLoader:
    "SchemaId & PackagedSinger -> Cmd[None]"
    _procedure: Callable[[SchemaId, PackagedSinger], Cmd[None]]

    def handle(self, schema: SchemaId, msg: PackagedSinger) -> Cmd[None]:
        return self._procedure(schema, msg)
