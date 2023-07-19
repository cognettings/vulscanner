# pylint: skip-file

from analytics.domain import (
    handle_authz_claims,
)
from analytics.types import (
    GraphicParameters,
    GraphicsCsvParameters,
    GraphicsForEntityParameters,
    ReportParameters,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
)
from unittest.mock import (
    MagicMock,
)

MOCK_DATA: Dict[str, Dict[str, Any]] = {
    "test_get_document": {
        "mock_analytics_dal_get_document": """
        {
            "vulnerabilities": 3,
            "max_severity": 2,
            "entity": "organization"
        }
        """
    },
    "test_handle_graphic_request_returns_graphic_error_template": {
        "mock_handle_graphic_request_parameters": GraphicParameters(
            document_name="testing",
            document_type="json",
            entity="organization",
            generator_name="generic",
            generator_type="c3",
            height=200,
            width=200,
            subject="testing",
        )
    },
    "test_handle_graphic_request_returns_graphic_template": {
        "mock_handle_graphic_request_parameters": GraphicParameters(
            document_name="testing",
            document_type="json",
            entity="organization",
            generator_name="generic",
            generator_type="c3",
            height=200,
            width=200,
            subject="testing",
        )
    },
    "test_handled_graphic_csv_request_catches_errors": {
        "mock_handle_graphic_csv_request_parameters": GraphicsCsvParameters(
            entity="group",
            subject="testing",
            document_type="csv",
            document_name="test_csv",
        )
    },
}


@pytest.fixture
def mock_data_for_module() -> Callable[[str, str], Any]:
    def _mock_data_for_module(
        test_name: str,
        mock_name: str,
    ) -> Any:
        return MOCK_DATA[test_name][mock_name]

    return _mock_data_for_module


@pytest.fixture(scope="module", autouse=True)
def download_fileobj() -> Generator:
    expected_content = "test document content"

    def mock_download_fileobj_wrapper(
        bucket: str, key: str, stream: Any
    ) -> None:
        stream.write(expected_content.encode())

    yield mock_download_fileobj_wrapper


@pytest_asyncio.fixture
def assert_permission_error() -> Callable:
    async def assert_permission_error_wrapper(
        params: (
            GraphicParameters
            | GraphicsCsvParameters
            | GraphicsForEntityParameters
            | ReportParameters
        ),
        request: MagicMock,
    ) -> None:
        with pytest.raises(PermissionError):
            await handle_authz_claims(params=params, request=request)

    return assert_permission_error_wrapper


@pytest.fixture
def request_fixture() -> MagicMock:
    return MagicMock()
