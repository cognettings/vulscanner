from collections.abc import (
    Callable,
)
import pytest
from typing import (
    Any,
)

pytestmark = [
    pytest.mark.asyncio,
]


class MockModule:
    # pylint: disable=too-few-public-methods
    """A dummy docstring."""

    def __init__(self) -> None:
        """init for test mock class"""

    def main(self) -> None:
        """A dummy docstring."""


MOCK_MODULE = MockModule()

MOCKED_DATA: dict[str, dict[str, Any]] = {
    "cli.invoker.dynamo_shutdown": {
        "[]": None,
    },
    "cli.invoker.dynamo_startup": {
        "[]": None,
    },
    "cli.invoker.sqs_shutdown": {
        "[]": None,
    },
    "cli.invoker.sqs_startup": {
        "[]": None,
    },
    "cli.invoker.importlib.import_module": {
        "[]": MOCK_MODULE,
    },
}


@pytest.fixture
def mocked_data_for_module(
    *,
    resolve_mock_data: Callable,
) -> Any:
    def _mocked_data_for_module(
        mock_path: str, mock_args: list[Any], module_at_test: str
    ) -> Callable[[str, list[Any], str], Any]:
        return resolve_mock_data(
            mock_data=MOCKED_DATA,
            mock_path=mock_path,
            mock_args=mock_args,
            module_at_test=module_at_test,
        )

    return _mocked_data_for_module
