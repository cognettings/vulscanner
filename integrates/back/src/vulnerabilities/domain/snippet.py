from contextlib import (
    suppress,
)
from custom_exceptions import (
    VulnNotFound,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
from git.exc import (
    GitCommandError,
)
from git.repo import (
    Repo,
)
import logging
from serializers import (
    make_snippet,
    Snippet,
    SnippetViewport,
)
from settings.logger import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def set_snippet(
    vulnerability: Vulnerability,
    contents: Snippet,
) -> None:
    try:
        modified_state = vulnerability.state._replace(snippet=contents)
        await vulns_model.update_historic_entry(
            current_value=vulnerability,
            finding_id=vulnerability.finding_id,
            vulnerability_id=vulnerability.id,
            entry=modified_state,
        )
    except VulnNotFound as exc:
        LOGGER.error(
            "Failed to set vulnerability snippet",
            extra={"extra": {"vulnerability_id": vulnerability.id}},
        )
        LOGGER.exception(exc)


def generate_snippet(
    vulnerability_state: VulnerabilityState, repo: Repo
) -> Snippet | None:
    current_commit = vulnerability_state.commit or "HEAD"
    with suppress(GitCommandError, ValueError):
        content = repo.git.show(
            f"{current_commit}:{vulnerability_state.where}"
        )
        return make_snippet(
            content=content,
            viewport=SnippetViewport(
                line=int(vulnerability_state.specific),
                column=0,
                show_line_numbers=False,
                highlight_line_number=False,
            ),
        )
    return None
