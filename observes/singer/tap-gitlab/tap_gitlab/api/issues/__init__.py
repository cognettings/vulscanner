from ._client import (
    IssueClient,
    IssueFilter,
)
from tap_gitlab.api.core.ids import (
    IssueId,
)
from tap_gitlab.api.core.issue import (
    Issue,
    IssueObj,
    IssueType,
)

__all__ = [
    "IssueId",
    "IssueType",
    "Issue",
    "IssueObj",
    "IssueFilter",
    "IssueClient",
]
