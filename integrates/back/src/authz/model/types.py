from typing import (
    TypedDict,
)


class RoleLevel(TypedDict):
    actions: set[str]
    tags: set[str]


RoleModel = dict[str, RoleLevel]
