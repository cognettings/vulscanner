from collections.abc import (
    Iterator,
)
from contextlib import (
    contextmanager,
)
from gql.client import (
    Client as GraphQLClient,
)
from gql.transport.requests import (
    RequestsHTTPTransport,
)
from gql.transport.transport import (
    Transport,
)


@contextmanager
def client(token_fluidattacks: str) -> Iterator[GraphQLClient]:
    transport: Transport = RequestsHTTPTransport(
        headers={"Authorization": f"Bearer {token_fluidattacks}"},
        timeout=20,
        url="https://app.fluidattacks.com/api",
    )
    yield GraphQLClient(
        transport=transport,
    )
