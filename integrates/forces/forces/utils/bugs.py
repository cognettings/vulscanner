from aiohttp.client_exceptions import (
    ClientConnectorError,
    ClientResponseError,
)
import bugsnag
from bugsnag.event import (
    Event,
)
from bugsnag_client import (
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from contextvars import (
    ContextVar,
)
from forces.model import (
    ForcesConfig,
)
from forces.utils.env import (
    BASE_DIR,
    guess_environment,
)
import os

# Constants
META: ContextVar[dict[str, str] | None] = ContextVar("META", default=None)


def customize_bugsnag_error_reports(
    event: Event,
) -> None:  # pragma: no cover
    # Customize Login required error
    environment = {}
    if os.environ.get("CI_JOB_ID", None):
        environment["PIPELINE"] = "GITLAB_CI"
        environment["CI_JOB_ID"] = os.environ.get("CI_JOB_ID", "unknown")
        environment["CI_JOB_URL"] = os.environ.get("CI_JOB_URL", "unknown")
    elif os.environ.get("CIRCLECI", None):
        environment["PIPELINE"] = "CIRCLECI"
        environment["CIRCLE_BUILD_NUM"] = os.environ.get(
            "CIRCLE_BUILD_NUM", "unknown"
        )
        environment["CIRCLE_BUILD_URL"] = os.environ.get(
            "CIRCLE_BUILD_URL", "unknown"
        )
    elif os.environ.get("System.JobId", None):
        environment["PIPELINE"] = "AZURE_DEVOPS"
        environment["System.JobId"] = os.environ.get("System.JobId", "unknown")
    elif os.environ.get("BUILD_NUMBER", None):
        environment["PIPELINE"] = "JENKINS"
        os.environ["BUILD_NUMBER"] = os.environ.get("BUILD_NUMBER", "unknown")
        os.environ["BUILD_ID"] = os.environ.get("BUILD_ID", "unknown")
        os.environ["BUILD_URL"] = os.environ.get("BUILD_URL", "unknown")
    event.add_tab("environment", environment)

    if isinstance(
        event.exception,
        (
            ClientConnectorError,
            ClientResponseError,
        ),
    ):
        login_error = any(
            (
                err in str(event.exception)
                for err in (
                    "Login required",
                    "Access denied",
                    "Token format unrecognized",
                )
            )
        )
        if login_error:
            event.severity = "info"
            event.unhandled = False
        else:
            event.severity = (
                "error" if guess_environment() == "production" else "warning"
            )
            event.unhandled = guess_environment() == "production"
    else:
        event.severity = (
            "error" if guess_environment() == "production" else "warning"
        )
        event.unhandled = guess_environment() == "production"


def configure_bugsnag(config: ForcesConfig) -> None:
    # Metadata configuration
    META.set(config._asdict())
    # Add before handler
    bugsnag.before_notify(customize_bugsnag_error_reports)
    bugsnag.before_notify(bugsnag_remove_nix_hash)
    # Initialization
    bugsnag.configure(
        # There is no problem in making this key public
        # it's intentional so we can monitor Skims stability in remote users
        api_key="3625546064ad4b5b78aa0c0c93919fc5",
        app_version=os.environ["CI_COMMIT_SHA"][0:8]
        if "CI_COMMIT_SHA" in os.environ
        else None,
        release_stage=guess_environment(),
        project_root=BASE_DIR,
        send_environment=True,
    )
    bugsnag.start_session()
