from back.test.unit.src.utils import (
    get_module_at_test,
)
from datetime import (
    datetime,
)
from freezegun import (
    freeze_time,
)
import pytest
from schedulers.update_group_toe_sorts import (
    main,
    process_group,
)
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@freeze_time("2020-12-01")
@pytest.mark.parametrize(
    ["group_name"],
    [["unittesting"]],
)
@patch(MODULE_AT_TEST + "update_sorts_attributes", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "S3_BUCKET.Object")
@patch(MODULE_AT_TEST + "tempfile.TemporaryDirectory")
@patch(MODULE_AT_TEST + "Dataloaders.group_toe_lines", new_callable=AsyncMock)
async def test_process_group(
    # pylint: disable=too-many-arguments
    mock_dataloaders_group_toe_lines: AsyncMock,
    mock_tempfile_temporary_directory: MagicMock,
    mock_s3_bucket_object: MagicMock,
    mock_update_sorts_attributes: AsyncMock,
    group_name: str,
    mocked_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_dataloaders_group_toe_lines.load_nodes,
            "Dataloaders.group_toe_lines",
            [group_name],
        ),
        (
            mock_tempfile_temporary_directory.return_value.__enter__,
            "tempfile.TemporaryDirectory",
            [group_name],
        ),
        (
            mock_s3_bucket_object.return_value.download_file,
            "S3_BUCKET.Object",
            [group_name],
        ),
        (
            mock_update_sorts_attributes,
            "update_sorts_attributes",
            [group_name, datetime.now()],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for item in mocks_setup_list:
        mock, path, arguments = item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    await process_group(group_name=group_name, current_date=datetime.now())

    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)


@patch(MODULE_AT_TEST + "process_group", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "orgs_domain.get_all_active_group_names",
    new_callable=AsyncMock,
)
async def test_update_group_toe_sorts(
    mock_orgs_domain_get_all_active_group_names: AsyncMock,
    mock_process_group: AsyncMock,
    mocked_data_for_module: Any,
) -> None:
    # Set up mock's result using mocked_data_for_module fixture
    mock_orgs_domain_get_all_active_group_names.return_value = (
        mocked_data_for_module(
            mock_path="orgs_domain.get_all_active_group_names",
            mock_args=[],
            module_at_test=MODULE_AT_TEST,
        )
    )

    # Functions inside collect have to be mocked using side_effect
    # so that the iterations work
    mock_process_group.side_effect = mocked_data_for_module(
        mock_path="process_group",
        mock_args=[],
        module_at_test=MODULE_AT_TEST,
    )
    await main()
    assert mock_orgs_domain_get_all_active_group_names.called is True
    assert mock_process_group.call_count == 11
