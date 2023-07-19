from azure.devops.v6_0.git.models import (
    GitRepository,
)
from db_model.azure_repositories.types import (
    BasicRepoData,
)
import logging
import logging.config
from settings.logger import (
    LOGGING,
)
from urllib.parse import (
    unquote_plus,
    urlparse,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


def does_not_exist_in_gitroot_urls(
    *,
    repository: GitRepository | BasicRepoData,
    urls: set[str],
    nicknames: set[str],
) -> bool:
    name_filter = str(repository.name).lower() in nicknames

    remote_url_filter = (
        unquote_plus(urlparse(repository.remote_url.lower()).path) in urls
    )
    ssh_url_filter = (
        unquote_plus(urlparse(repository.ssh_url.lower()).path) in urls
        or unquote_plus(urlparse(f"ssh://{repository.ssh_url.lower()}").path)
        in urls
    )
    web_url_filter = (
        unquote_plus(urlparse(repository.web_url.lower()).path) in urls
    )

    return not any(
        [name_filter, remote_url_filter, ssh_url_filter, web_url_filter]
    )
