from operator import (
    itemgetter,
)
from typing import (
    NamedTuple,
)
import yaml


class ValueToAdd(NamedTuple):
    data: dict[str, int]

    def add(self, element: str) -> None:
        self.data.setdefault(element, 0)
        self.data[element] += 1

    def is_not_empty(self) -> bool:
        return bool(len(self.data))

    def __str__(self) -> str:
        data = [
            f"{occurrences} - {element}"
            for element, occurrences in sorted(
                self.data.items(),
                key=itemgetter(1),
                reverse=True,
            )
        ]
        return yaml.safe_dump(data)
