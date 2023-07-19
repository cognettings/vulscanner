from collections import (
    UserList,
)
from collections.abc import (
    Iterable,
)


class ListToken(UserList):
    def __init__(
        self,
        value: Iterable[object],
        line: int = 0,
        column: int = 0,
    ):
        super().__init__(value)
        self.__line__ = line
        self.__column__ = column
