from collections.abc import (
    Iterator,
)
from forces.model import (
    ForcesConfig,
)
import os
import pytest


@pytest.fixture(scope="session")
def test_org() -> Iterator[str]:
    yield "okada"


@pytest.fixture(scope="session")
def test_group() -> Iterator[str]:
    yield "unittesting"


@pytest.fixture(scope="session")
def test_finding() -> Iterator[str]:
    yield "422286126"


@pytest.fixture(scope="session")
def test_token() -> Iterator[str]:
    yield os.environ["TEST_FORCES_TOKEN"]


@pytest.fixture(scope="session")
def test_endpoint() -> Iterator[str]:
    yield "https://127.0.0.1:8001/api"


@pytest.fixture(scope="session")
def test_config() -> Iterator[ForcesConfig]:
    yield ForcesConfig(
        organization="okada",
        group="unittesting",
    )
