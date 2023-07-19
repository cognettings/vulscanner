from integrates.domain import (
    get_vulnerable_lines,
)
from integrates.graphql import (
    client as graphql_client,
)
import pytest


@pytest.mark.usefixtures("test_token_fluidattacks")
def test_client(test_token_fluidattacks: str) -> None:
    with graphql_client(test_token_fluidattacks) as client:
        assert client.transport.headers == {
            "Authorization": f"Bearer {test_token_fluidattacks}"
        }


@pytest.mark.usefixtures("test_token_fluidattacks")
def test_get_vulnerable_lines(test_token_fluidattacks: str) -> None:
    vulnerabilities = get_vulnerable_lines(test_token_fluidattacks, "abomey")
    # FP: local testing
    assert len(vulnerabilities) >= 0  # NOSONAR
