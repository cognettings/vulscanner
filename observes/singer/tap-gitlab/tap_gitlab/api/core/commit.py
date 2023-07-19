from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)


@dataclass(frozen=True)
class Commit:
    author_email: str
    author_name: str
    authored_date: datetime
    committer_email: str
    committer_name: str
    committed_date: datetime
    created_at: datetime
    message: str
    title: str
