from back.test.unit.src.utils import (
    get_module_at_test,
)
from custom_exceptions import (
    DocumentNotFound,
    UnavailabilityError,
)
from graphql import (
    GraphQLError,
)
import logging
import pytest
from settings import (
    LOGGING,
)
from settings.logger import (
    customize_bugsnag_error_reports,
)
from unittest.mock import (
    MagicMock,
    Mock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


@patch(MODULE_AT_TEST + "bugsnag_remove_nix_hash", Mock(side_effect=None))
def test_customize_bugsnag_error_reports_returns_false() -> None:
    notification = MagicMock()
    attrs = {
        "exception": GraphQLError("Testing"),
        "grouping_hash": "testing",
        "errors": [MagicMock()],
    }
    notification.configure_mock(**attrs)
    assert not customize_bugsnag_error_reports(notification)


@pytest.mark.parametrize(
    ["error"],
    [
        [DocumentNotFound()],
        [UnavailabilityError({})],
    ],
)
@patch(MODULE_AT_TEST + "bugsnag_remove_nix_hash", Mock(side_effect=None))
def test_customize_bugsnag_error_reports_returns_true(
    error: Exception,
) -> None:
    notification = MagicMock()
    original_error = MagicMock()
    original_error.configure_mock(
        **{
            "stacktrace": [
                {"file": "integrates/back/migration/0399_fix_queue_state.py"}
            ]
        }
    )
    attrs = {
        "exception": error,
        "grouping_hash": "testing",
        "errors": [original_error],
    }
    notification.configure_mock(**attrs)
    assert customize_bugsnag_error_reports(notification)


@patch(MODULE_AT_TEST + "bugsnag_remove_nix_hash", Mock(side_effect=None))
def test_customize_bugsnag_error_migrations_report() -> None:
    notification = MagicMock()
    original_error = MagicMock()
    original_error.configure_mock(
        **{
            "stacktrace": [
                {"file": "integrates/back/migrations/0399_fix_queue_state.py"}
            ]
        }
    )
    attrs = {
        "exception": Exception({"Error": "from migration"}),
        "grouping_hash": "testing",
        "errors": [original_error],
        "unhandled": True,
        "severity": "error",
    }
    notification.configure_mock(**attrs)
    assert customize_bugsnag_error_reports(notification)
    assert not notification.unhandled
    assert notification.severity == "info"
