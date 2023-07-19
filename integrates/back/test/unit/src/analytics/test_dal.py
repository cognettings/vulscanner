from analytics.dal import (
    get_document,
    get_snapshot,
)
from back.test.unit.src.utils import (
    get_module_at_test,
)
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
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(["key"], [["nonexistent_document.txt"]])
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_get_document_raises_document_not_found(
    mock_get_s3_resource: AsyncMock,
    key: str,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_client.download_fileobj.side_effect = ClientError(
        {}, "download_fileobj"
    )
    with pytest.raises(DocumentNotFound):
        await get_document(key=key)


@pytest.mark.parametrize(["key"], [["existing_document.txt"]])
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_get_document_returns_document_content(
    mock_get_s3_resource: AsyncMock,
    download_fileobj: Any,
    key: str,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_download_fileobj = mock_client.download_fileobj
    mock_download_fileobj.side_effect = download_fileobj
    actual_content = await get_document(key=key)
    assert actual_content == "test document content"


@pytest.mark.parametrize(["key"], [["nonexistent_document.txt"]])
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_get_snapshot_raises_snapshot_not_found(
    mock_get_s3_resource: AsyncMock,
    key: str,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_client.download_fileobj.side_effect = ClientError(
        {}, "download_fileobj"
    )
    with pytest.raises(SnapshotNotFound):
        await get_snapshot(key=key)
    assert mock_client.download_fileobj.await_count == 3


@pytest.mark.parametrize(["key"], [["existing_document.txt"]])
@patch(MODULE_AT_TEST + "get_s3_resource", new_callable=AsyncMock)
async def test_get_snapshot_returns_document_content(
    mock_get_s3_resource: AsyncMock,
    download_fileobj: Any,
    key: str,
) -> None:
    mock_client = mock_get_s3_resource.return_value
    mock_download_fileobj = mock_client.download_fileobj
    mock_download_fileobj.side_effect = download_fileobj
    actual_content = await get_snapshot(key=key)
    assert actual_content == b"test document content"
