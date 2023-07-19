from custom_utils.organizations import (
    get_organization_country,
)
from typing import (
    NamedTuple,
)


class Context(NamedTuple):
    headers: dict[str, str]


def test_get_organization_country() -> None:
    inputs = [Context(headers={"cf-ipcountry": "CO"}), Context(headers={})]
    outputs: list[str] = ["Colombia", "undefined"]
    for index, context in enumerate(inputs):
        assert outputs[index] == get_organization_country(context)
