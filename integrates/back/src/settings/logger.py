# Settings logger-related configs


from .various import (
    BASE_DIR,
    DEBUG,
)
from aioextensions import (
    in_thread,
    schedule,
)
import asyncio
from boto3.session import (
    Session,
)
import bugsnag
from bugsnag.notification import (
    Notification,
)
from bugsnag_client import (
    remove_nix_hash as bugsnag_remove_nix_hash,
)
from context import (
    CI_COMMIT_SHA,
    CI_COMMIT_SHORT_SHA,
    FI_AWS_REGION_NAME,
    FI_BUGSNAG_API_KEY_BACK,
    FI_ENVIRONMENT,
    LOG_LEVEL_BUGSNAG,
    LOG_LEVEL_CONSOLE,
    LOG_LEVEL_WATCHTOWER,
)
from custom_exceptions import (
    DocumentNotFound,
    UnavailabilityError,
)
from graphql import (
    GraphQLError,
)
import json
from logging import (
    Filter,
    Formatter,
    LogRecord,
    StreamHandler,
)
import logging.config
import os
import re
import requests
from requests.exceptions import (
    ConnectionError as RequestConnectionError,
    ReadTimeout,
)
from typing import (
    Literal,
)

BOTO3_SESSION = Session(
    region_name=FI_AWS_REGION_NAME,
)


# pylint: disable=too-few-public-methods
class RequireDebugFalse(Filter):
    def filter(self, _: LogRecord) -> bool:
        return not DEBUG


class ExtraMessageFormatter(Formatter):
    def __init__(
        self,
        fmt: str = "[{levelname}] {message}, extra={extra}",
        style: Literal["{"] = "{",
    ) -> None:
        logging.Formatter.__init__(self, fmt=fmt, style=style)

    def format(self, record: LogRecord) -> str:
        arg_pattern = re.compile(r"\{(\w+)\}")
        arg_names = [x.group(1) for x in arg_pattern.finditer(str(self._fmt))]
        for field in arg_names:
            if field not in record.__dict__:
                record.__dict__[field] = None

        return super().format(record)


class AsyncStreamHandler(StreamHandler):
    def emit(self, record: LogRecord) -> None:
        try:
            asyncio.get_running_loop()
            schedule(in_thread(super().emit, record))
        except RuntimeError:
            # Called outside an async context
            super().emit(record)


MODULES = os.listdir(os.path.dirname(os.path.dirname(__file__)))
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": RequireDebugFalse},
    },
    "formatters": {
        "level_message_extra": {
            "()": ExtraMessageFormatter,
        },
    },
    "handlers": {
        "bugsnag": {
            "extra_fields": {"extra": ["extra"]},
            "filters": ["require_debug_false"],
            "class": "bugsnag.handlers.BugsnagHandler",
            "level": LOG_LEVEL_BUGSNAG or "WARNING",
        },
        "console": {
            "()": AsyncStreamHandler,
            "level": LOG_LEVEL_CONSOLE or "INFO",
            "formatter": "level_message_extra",
        },
        "watchtower": {
            "boto3_client": BOTO3_SESSION.client("logs"),
            "class": "watchtower.CloudWatchLogHandler",
            # Since LogGroup already exists, it was causing a
            # ThrottlingException error that resulted in 'unable to configure
            # watchtower'
            "create_log_group": False,
            "create_log_stream": False,
            "filters": ["require_debug_false"],
            "level": LOG_LEVEL_WATCHTOWER or "INFO",
            "log_group_name": "FLUID",
            "log_stream_name": "FLUIDIntegrates",
            "use_queues": True,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "transactional": {
            "handlers": ["watchtower"],
            "level": "INFO",
        },
        **{
            module: {
                "handlers": ["bugsnag"],
                "level": "INFO",
            }
            for module in MODULES
        },
    },
}

# Force logging to load the config right away
# This is important otherwise loggers are not going to work in CI jobs
logging.config.dictConfig(LOGGING)


# bugsnag
bugsnag.configure(
    api_key=FI_BUGSNAG_API_KEY_BACK,
    app_version=CI_COMMIT_SHORT_SHA,
    asynchronous=True,
    auto_capture_sessions=True,
    project_root=BASE_DIR,
    release_stage=FI_ENVIRONMENT,
    send_environment=True,
)

if FI_ENVIRONMENT == "production":
    URL = "https://build.bugsnag.com"
    HEADERS = {"Content-Type": "application/json", "server": "None"}
    PAYLOAD = {
        "apiKey": FI_BUGSNAG_API_KEY_BACK,
        "appVersion": CI_COMMIT_SHORT_SHA,
        "releaseStage": FI_ENVIRONMENT,
        "sourceControl": {
            "provider": "gitlab",
            "repository": "https://gitlab.com/fluidattacks/universe.git",
            "revision": f"{CI_COMMIT_SHA}/integrates/back/packages",
        },
    }
    try:
        requests.post(
            URL, headers=HEADERS, data=json.dumps(PAYLOAD), timeout=3
        )
    except (ReadTimeout, RequestConnectionError) as exc:
        logging.exception(exc, f"request to {URL} was not completed")


def customize_bugsnag_error_reports(notification: Notification) -> bool:
    """Handle for expected errors and customization"""
    bugsnag_remove_nix_hash(notification)
    ex_msg = str(notification.exception)

    notification.grouping_hash = ex_msg
    if isinstance(notification.exception, GraphQLError):
        return False
    if isinstance(notification.exception, UnavailabilityError):
        notification.unhandled = False
    if isinstance(notification.exception, DocumentNotFound):
        notification.severity = "info"
    if notification.errors:
        errors_messages = [
            trace.get("file", "")
            for error in notification.errors
            for trace in error.stacktrace
        ]
        if "/migrations/" in "".join(errors_messages):
            notification.unhandled = False
            notification.severity = "info"

    if not (
        "ec2" in notification.hostname or "integrates" in notification.hostname
    ):
        notification.unhandled = False
    return True


bugsnag.before_notify(customize_bugsnag_error_reports)
