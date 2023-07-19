from dataclasses import (
    dataclass,
)
from typing import (
    FrozenSet,
)


class TokenGenerationFail(Exception):
    pass


@dataclass(frozen=True)
class Token:
    raw_token: str

    def __repr__(self) -> str:
        return "[masked]"


@dataclass(frozen=True)
class RefreshToken:
    raw_token: str

    def __repr__(self) -> str:
        return "[masked]"


@dataclass(frozen=True)
class Credentials:
    client_id: str
    client_secret: str
    refresh_token: str
    scopes: FrozenSet[str]

    def __repr__(self) -> str:
        return f"Creds(client_id={self.client_id}, scopes={self.scopes})"
