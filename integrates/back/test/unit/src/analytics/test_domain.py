from analytics.domain import (
    get_csv_document,
    get_document,
    get_graphics_report,
    handle_authz_claims,
    handle_graphic_csv_request,
    handle_graphic_request,
    handle_graphic_request_parameters,
    handle_graphics_csv_request_parameters,
    handle_graphics_for_entity_request,
    handle_graphics_for_entity_request_parameters,
    handle_graphics_report_request,
    handle_graphics_report_request_parameters,
)
from analytics.types import (
    GraphicParameters,
    GraphicsCsvParameters,
    GraphicsForEntityParameters,
    ReportParameters,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
import base64
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    DocumentNotFound,
    SnapshotNotFound,
)
import pytest
from typing import (
    Any,
    Callable,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    Mock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["document_name", "document_type", "entity", "subject"],
    [
        (
            "camelCaseDocumentNameToTest",
            "c3",
            "group",
            "non-existent_doc",
        ),
        (
            "snake_case_name_",
            "BartChart",
            "organization",
            "",
        ),
    ],
)
async def test_get_csv_document(
    document_name: str,
    document_type: str,
    entity: str,
    subject: str,
) -> None:
    with pytest.raises(DocumentNotFound):
        await get_csv_document(
            document_name=document_name,
            document_type=document_type,
            entity=entity,
            subject=subject,
        )


@pytest.mark.parametrize(
    ["document_name", "document_type", "entity", "subject"],
    [
        (
            "DocumentName",
            "documentType",
            "group",
            "group_id",
        ),
    ],
)
@patch(MODULE_AT_TEST + "analytics_dal.get_document", new_callable=AsyncMock)
async def test_get_document(
    # pylint: disable=too-many-arguments
    mock_analytics_dal_get_document: AsyncMock,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str,
    mock_data_for_module: Callable[[str, str], Any],
) -> None:
    mock_analytics_dal_get_document.return_value = mock_data_for_module(
        "test_get_document", "mock_analytics_dal_get_document"
    )
    result = await get_document(
        document_name=document_name,
        document_type=document_type,
        entity=entity,
        subject=subject,
    )
    assert result == {
        "vulnerabilities": 3,
        "max_severity": 2,
        "entity": "organization",
    }


@patch(MODULE_AT_TEST + "analytics_dal.get_snapshot", return_value=bytes(2))
async def test_get_graphics_report(
    mock_analytics_dal_get_snapshot: AsyncMock,
) -> None:
    assert await get_graphics_report(
        entity="", subject="test"
    ) == base64.b64encode(bytes(2))
    mock_analytics_dal_get_snapshot.assert_awaited_once_with(
        "reports/:74657374.png"
    )


@patch(
    MODULE_AT_TEST + "analytics_dal.get_snapshot",
    side_effect=SnapshotNotFound(),
)
async def test_get_graphics_report_snapshot_not_found(
    mock_analytics_dal_get_snapshot: AsyncMock,
) -> None:
    with pytest.raises(SnapshotNotFound):
        await get_graphics_report(entity="", subject="test")
    mock_analytics_dal_get_snapshot.assert_awaited_once_with(
        "reports/:74657374.png"
    )


@pytest.mark.parametrize(
    ["params"],
    [
        [
            GraphicParameters(
                document_name="test_document",
                document_type="csv",
                entity="group",
                generator_type="barChar",
                generator_name="generic",
                subject="testing",
                height=200,
                width=200,
            )
        ],
        [
            GraphicsForEntityParameters(
                entity="organization", subject="testing"
            )
        ],
        [ReportParameters(entity="portfolio", subject="testing")],
        [
            GraphicsCsvParameters(
                document_name="testing_document",
                document_type="json",
                entity="invalid_entity",
                subject="testing_60",
            )
        ],
    ],
)
@patch(
    MODULE_AT_TEST + "sessions_domain.get_jwt_content", new_callable=AsyncMock
)
async def test_handle_authz_claims(
    mock_get_jwt_content: AsyncMock,
    params: (
        GraphicParameters
        | GraphicsCsvParameters
        | GraphicsForEntityParameters
        | ReportParameters
    ),
    assert_permission_error: Callable,
) -> None:
    mock_get_jwt_content.return_value = {
        "user_email": "testing@fluidattacks.com"
    }
    request = MagicMock()
    if params.entity == "group":
        with patch(MODULE_AT_TEST + "authz.has_access_to_group") as mock_authz:
            mock_authz.return_value = False
            await assert_permission_error(params=params, request=request)
    elif params.entity == "organization":
        with patch(
            MODULE_AT_TEST + "orgs_access.has_access"
        ) as mock_org_access:
            mock_org_access.return_value = False
            await assert_permission_error(params=params, request=request)
    elif params.entity == "portfolio":
        with patch(
            MODULE_AT_TEST + "tags_domain.has_access"
        ) as mock_tags_domain:
            mock_tags_domain.return_value = False
            await assert_permission_error(params=params, request=request)
    else:
        with pytest.raises(ValueError):
            await handle_authz_claims(params=params, request=request)


@patch(MODULE_AT_TEST + "handle_graphic_request_parameters")
@patch(MODULE_AT_TEST + "handle_authz_claims", return_value=None)
async def test_handle_graphic_request_returns_graphic_error_template(
    mock_handle_authz_claims: AsyncMock,
    mock_handle_graphic_request_parameters: MagicMock,
    mock_data_for_module: Callable[[str, str], Any],
) -> None:
    request = MagicMock()
    request.configure_mock(
        query_params={"error_info": "testing"}, url={"url": "/testing"}
    )
    with patch(
        MODULE_AT_TEST + "handle_graphic_request_parameters",
    ) as mock_handle_graphic_parameters:
        mock_handle_graphic_parameters.side_effect = ValueError("testing")
        response = await handle_graphic_request(request)
        assert response.template.name == "graphic-error.html"  # type: ignore

    mock_handle_graphic_request_parameters.return_value = mock_data_for_module(
        "test_handle_graphic_request_returns_graphic_error_template",
        "mock_handle_graphic_request_parameters",
    )
    with patch(
        MODULE_AT_TEST + "get_document", new_callable=AsyncMock
    ) as mock_get_document_not_found_error:
        mock_get_document_not_found_error.side_effect = DocumentNotFound()
        response = await handle_graphic_request(request)
        mock_handle_authz_claims.assert_awaited_once()
        assert response.template.name == "graphic-error.html"  # type: ignore


@patch(MODULE_AT_TEST + "handle_graphic_request_parameters")
@patch(MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_document", new_callable=AsyncMock)
async def test_handle_graphic_request_returns_graphic_template(
    mock_get_document: AsyncMock,
    mock_handle_authz_claims: AsyncMock,
    mock_handle_graphic_request_parameters: Mock,
    request_fixture: MagicMock,
    mock_data_for_module: Callable[[str, str], Any],
) -> None:
    mock_handle_authz_claims.return_value = None
    mock_handle_graphic_request_parameters.return_value = mock_data_for_module(
        "test_handle_graphic_request_returns_graphic_template",
        "mock_handle_graphic_request_parameters",
    )
    mock_get_document.return_value = dict(title="testing", source="s3_bucket")
    response = await handle_graphic_request(request_fixture)
    assert response.template.name == "graphic.html"  # type: ignore
    graphic_info = response.context["args"]["data"]  # type: ignore
    assert graphic_info == '{"title": "testing", "source": "s3_bucket"}'
    assert response.context["args"]["height"] == 200  # type: ignore


@patch(MODULE_AT_TEST + "handle_graphics_csv_request_parameters")
@patch(MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_csv_document", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "LOGGER.exception")
async def test_handled_graphic_csv_request_catches_errors(
    # pylint: disable=too-many-arguments
    mock_logger_exception: Mock,
    mock_get_csv_document: AsyncMock,
    mock_handle_authz_claims: AsyncMock,
    mock_handle_graphic_csv_request_parameters: Mock,
    request_fixture: MagicMock,
    mock_data_for_module: Callable[[str, str], Any],
) -> None:
    mock_logger_exception.side_effect = None
    with patch(
        MODULE_AT_TEST + "handle_graphics_csv_request_parameters"
    ) as mock_csv_request:
        mock_csv_request.side_effect = ValueError(
            "Error raised from handle_graphics_csv_request_parameters"
        )
        response = await handle_graphic_csv_request(request_fixture)
        assert response.template.name == "graphic-error.html"  # type: ignore

    mock_handle_graphic_csv_request_parameters.return_value = (
        mock_data_for_module(
            "test_handled_graphic_csv_request_catches_errors",
            "mock_handle_graphic_csv_request_parameters",
        )
    )
    with patch(
        MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock
    ) as mock_authz:
        mock_authz.side_effect = ValueError("Error raised from authz")
        response = await handle_graphic_csv_request(request_fixture)
        assert response.template.name == "graphic-error.html"  # type: ignore

    mock_handle_authz_claims.return_value = None
    mock_get_csv_document.side_effect = DocumentNotFound()
    response = await handle_graphic_csv_request(request_fixture)
    assert response.template.name == "graphic-error.html"  # type: ignore
    assert mock_logger_exception.call_count == 3


@patch(MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "LOGGER.exception")
async def test_handle_graphic_for_entity_request_catches_errors(
    mock_logger_exception: Mock,
    mock_handle_authz_claims: AsyncMock,
    request_fixture: MagicMock,
) -> None:
    mock_handle_authz_claims.side_effect = PermissionError("testing error")
    mock_logger_exception.side_effect = None
    response = await handle_graphics_for_entity_request(
        entity="organization", request=request_fixture
    )
    assert response.template.name == "graphic-error.html"  # type: ignore
    mock_logger_exception.assert_called_once()


@patch(MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock)
async def test_handle_graphic_for_entity_request_returns_graphic_template(
    mock_handle_authz_claims: AsyncMock,
    request_fixture: MagicMock,
) -> None:
    mock_handle_authz_claims.side_effect = None
    response = await handle_graphics_for_entity_request(
        entity="organization", request=request_fixture
    )
    assert response.template.name == "graphics-for-entity.html"  # type: ignore
    assert response.context["entity"] == "Organization"  # type: ignore


@patch(MODULE_AT_TEST + "handle_graphics_report_request_parameters")
@patch(MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_graphics_report", new_callable=AsyncMock)
async def test_handle_graphic_report_request(
    mock_get_graphics_report: AsyncMock,
    mock_handle_authz_claims: AsyncMock,
    mock_handle_graphics_report_request_parameters: Mock,
    request_fixture: MagicMock,
) -> None:
    mock_handle_graphics_report_request_parameters.return_value = (
        ReportParameters(entity="group", subject="testing")
    )
    mock_handle_authz_claims.side_effect = None
    mock_get_graphics_report.return_value = bytes(5)
    response = await handle_graphics_report_request(request_fixture)
    assert response.status_code == 200
    assert response.media_type == "image/png"


@patch(MODULE_AT_TEST + "handle_graphics_report_request_parameters")
@patch(MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_graphics_report", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "LOGGER.exception")
async def test_handle_graphics_report_request_caches_errors(
    mock_logger_exception: Mock,
    mock_get_graphics_report: AsyncMock,
    mock_handle_authz_claims: AsyncMock,
    mock_handle_graphics_report_request_parameters: Mock,
    request_fixture: MagicMock,
) -> None:
    mock_logger_exception.side_effect = None
    mock_get_graphics_report.side_effect = ClientError(
        dict(Error={"Message": "snapshot not found"}), {}
    )
    with patch(
        MODULE_AT_TEST + "handle_graphics_report_request_parameters"
    ) as mock_request_parameters:
        mock_request_parameters.side_effect = ValueError(
            "testing handle_graphic_report_request"
        )
        response = await handle_graphics_report_request(request_fixture)
        assert response.template.name == "graphic-error.html"  # type: ignore
        mock_request_parameters.assert_called_once()

    mock_handle_graphics_report_request_parameters.return_value = (
        ReportParameters(entity="group", subject="testing")
    )
    with patch(
        MODULE_AT_TEST + "handle_authz_claims", new_callable=AsyncMock
    ) as mock_authz_claims:
        mock_authz_claims.side_effect = PermissionError("Access denied")
        response = await handle_graphics_report_request(request_fixture)
        mock_authz_claims.assert_called_once()
        assert response.template.name == "graphic-error.html"  # type: ignore

    mock_handle_authz_claims.side_effect = None
    response = await handle_graphics_report_request(request_fixture)
    assert response.template.name == "graphic-error.html"  # type: ignore
    assert mock_logger_exception.call_count == 3


@pytest.mark.parametrize(
    ["query_params", "error_message"],
    [
        [
            {"entity": "invalid entity", "invalid entity": "subject"},
            r'Invalid entity, only "group", "organization" and "portfolio" are valid',  # noqa: E501 pylint: disable=line-too-long
        ],
    ],
)
def test_handle_graphics_report_request_parameters_raises_error(
    request_fixture: MagicMock,
    query_params: dict[str, str],
    error_message: str,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    with pytest.raises(ValueError, match=error_message):
        handle_graphics_report_request_parameters(request=request)


@pytest.mark.parametrize(
    ["query_params"],
    [
        [{"entity": "group", "group": "testing"}],
    ],
)
def test_handle_graphics_report_request_parameters(
    request_fixture: MagicMock,
    query_params: dict[str, str],
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    response = handle_graphics_report_request_parameters(request=request)
    assert response.entity == "group"
    assert response.subject == "testing"


@pytest.mark.parametrize(
    ["entity", "query_params", "error_message"],
    [
        [
            "invalid entity",
            {"invalid_entity": "subject"},
            r'Invalid entity, only "group", "organization" and "portfolio" are valid',  # noqa: E501 pylint: disable=line-too-long
        ],
    ],
)
def test_handle_graphic_for_entity_request_parameters_raises_errors(
    request_fixture: MagicMock,
    entity: str,
    query_params: dict,
    error_message: str,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    with pytest.raises(ValueError, match=error_message):
        handle_graphics_for_entity_request_parameters(
            entity=entity, request=request
        )


@pytest.mark.parametrize(
    ["entity", "query_params"],
    [
        [
            "group",
            {"group": "testing"},
        ],
    ],
)
def test_handle_graphic_for_entity_request_parameters(
    request_fixture: MagicMock,
    entity: str,
    query_params: dict,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    response = handle_graphics_for_entity_request_parameters(
        entity=entity, request=request
    )
    assert response.entity == "group"
    assert response.subject == "testing"


@pytest.mark.parametrize(
    ["query_params", "error_message"],
    [
        [
            {
                "entity": "invalid entity",
                "subject": "testing",
                "documentName": "test",
                "documentType": "csv",
            },
            r'Invalid entity, only "group", "organization" and "portfolio" are valid',  # noqa: E501 pylint: disable=line-too-long
        ],
    ],
)
def test_handle_graphics_csv_request_parameters_raises_errors(
    request_fixture: MagicMock,
    query_params: dict,
    error_message: str,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    with pytest.raises(ValueError, match=error_message):
        handle_graphics_csv_request_parameters(request=request)


@pytest.mark.parametrize(
    ["query_params"],
    [
        [
            {
                "entity": "group",
                "subject": "testing",
                "documentName": "test",
                "documentType": "csv",
            },
        ],
    ],
)
def test_handle_graphics_csv_request_parameters(
    request_fixture: MagicMock,
    query_params: dict,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    response = handle_graphics_csv_request_parameters(request=request)
    assert response.entity == "group"
    assert response.subject == "testing"
    assert response.document_name == "test"
    assert response.document_type == "csv"


@pytest.mark.parametrize(
    ["query_params", "error_message"],
    [
        [
            {
                "entity": "portfolio",
                "subject": "testing",
                "documentName": "test",
                "documentType": "csv",
                "generatorName": "generic",
                "generatorType": "invalid generator type",
                "height": "300",
                "width": "600",
            },
            r"Invalid generator type",
        ],
        [
            {
                "entity": "portfolio",
                "subject": "testing",
                "documentName": "test",
                "documentType": "csv",
                "generatorName": "invalid name",
                "generatorType": "textBox",
                "height": "300",
                "width": "600",
            },
            r"Invalid generator name",
        ],
    ],
)
def test_handle_graphic_request_parameters_raises_errors(
    request_fixture: MagicMock,
    query_params: dict,
    error_message: str,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    with pytest.raises(ValueError, match=error_message):
        handle_graphic_request_parameters(request=request)


@pytest.mark.parametrize(
    ["query_params"],
    [
        [
            {
                "entity": "group",
                "subject": "testing",
                "documentName": "test",
                "documentType": "csv",
                "generatorName": "generic",
                "generatorType": "stackedBarChart",
                "height": "300",
                "width": "600",
            },
        ],
    ],
)
def test_handle_graphic_request_parameters(
    request_fixture: MagicMock,
    query_params: dict,
) -> None:
    request = request_fixture
    request.configure_mock(query_params=query_params)
    response = handle_graphic_request_parameters(request=request)
    assert response.entity == "group"
    assert response.generator_type == "stackedBarChart"
    assert response.width == 600
