from back.test.unit.src.utils import (
    get_module_at_test,
    set_mocks_return_values,
)
import os
import pytest
from resources.domain import (
    remove_file,
    save_file,
    search_file,
)
from starlette.datastructures import (
    UploadFile,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["file_name", "content_type"],
    [
        ["billing-test-file.png", "image/png"],
        ["unittesting-test-file.csv", "text/csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.upload_memory_file", new_callable=AsyncMock)
async def test_save_file(
    mock_s3_ops_upload_memory_file: AsyncMock,
    file_name: str,
    content_type: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_upload_memory_file],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.upload_memory_file"],
    )

    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data.name, data, content_type)
        await save_file(file_object=test_file, file_name=file_name)
    mock_s3_ops_upload_memory_file.assert_called_with(
        test_file, f"resources/{file_name}"
    )


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.list_files", new_callable=AsyncMock)
async def test_search_file(
    mock_s3_ops_list_files: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_list_files],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.list_files"],
    )

    assert file_name in await search_file(file_name)
    mock_s3_ops_list_files.assert_called_with(f"resources/{file_name}")


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.remove_file", new_callable=AsyncMock)
async def test_remove_file(
    mock_s3_ops_remove_file: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_remove_file],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.remove_file"],
    )

    await remove_file(file_name)
    mock_s3_ops_remove_file.assert_called_with(f"resources/{file_name}")
