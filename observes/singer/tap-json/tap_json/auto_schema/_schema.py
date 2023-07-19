from ._types import (
    SupportedTypes,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
)
from fa_purity.frozen import (
    freeze,
)


@dataclass(frozen=True)
class MutableSchema:
    _data: dict[str, frozenset[SupportedTypes]]

    def append(self, key: str, _type: SupportedTypes) -> Cmd[None]:
        def _action() -> None:
            if key not in self._data:
                self._data[key] = frozenset([_type])
            else:
                self._data[key].union([_type])

        return Cmd.from_cmd(_action)

    def get_schema(self) -> Cmd[FrozenDict[str, frozenset[SupportedTypes]]]:
        def _action() -> FrozenDict[str, frozenset[SupportedTypes]]:
            return freeze(self._data)

        return Cmd.from_cmd(_action)


@dataclass(frozen=True)
class MutableSchemaMap:
    _data: dict[str, MutableSchema]

    def get_or_create(self, table: str) -> Cmd[MutableSchema]:
        def _action() -> MutableSchema:
            if table not in self._data:
                self._data[table] = MutableSchema({})
            return self._data[table]

        return Cmd.from_cmd(_action)

    def append(self, table: str, key: str, _type: SupportedTypes) -> Cmd[None]:
        return self.get_or_create(table).bind(lambda ms: ms.append(key, _type))

    def get_map(self) -> Cmd[FrozenDict[str, MutableSchema]]:
        def _action() -> FrozenDict[str, MutableSchema]:
            return freeze(self._data)

        return Cmd.from_cmd(_action)

    def get_full_map(
        self,
    ) -> Cmd[FrozenDict[str, FrozenDict[str, frozenset[SupportedTypes]]]]:
        def _action(
            schemas: FrozenDict[str, MutableSchema], unwrapper: CmdUnwrapper
        ) -> FrozenDict[str, FrozenDict[str, frozenset[SupportedTypes]]]:
            return FrozenDict(
                {k: unwrapper.act(v.get_schema()) for k, v in schemas.items()}
            )

        return self.get_map().bind(
            lambda d: Cmd.new_cmd(lambda u: _action(d, u))
        )
