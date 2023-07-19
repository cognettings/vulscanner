from ..types import (
    PRIMARY_KEY_TEST,
    STR_MDL_REMOVE,
    TABLE,
)
from db_model.advisories.remove import (
    batch_remove,
    remove,
)
from dynamodb.types import (
    PrimaryKey,
)
from importlib import (
    import_module,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from unittest.mock import (
    Mock,
)


@pytest.fixture(name="mock_builtins_print")
def fixture_builtins_print(mocker: MockerFixture) -> Mock:
    return mocker.patch("builtins.print")


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_batch_remove(mocker: MockerFixture) -> None:
    platform = "npm"
    pkg_name = "package1"
    advisory_id = "ADV-001"
    source = "SOURCE"
    module_remove = import_module(STR_MDL_REMOVE)
    primary_key = PrimaryKey("test", "test")
    mocker.patch.object(module_remove, "TABLE", TABLE)
    mock_build_key = mocker.patch(
        f"{STR_MDL_REMOVE}.keys.build_key", return_value=primary_key
    )
    items = [{"pk": "pk_value", "sk": "sk_value"}]
    mock_query = mocker.patch(
        f"{STR_MDL_REMOVE}.operations.query",
        return_value=mocker.Mock(items=items),
    )
    mock_batch_delete_item = mocker.patch(
        f"{STR_MDL_REMOVE}.operations.batch_delete_item"
    )
    mock_print = mocker.patch("builtins.print")
    await batch_remove(
        platform=platform,
        pkg_name=pkg_name,
        advisory_id=advisory_id,
        source=source,
    )
    assert mock_build_key.call_args.kwargs == {
        "facet": TABLE.facets["advisories"],
        "values": {
            "platform": platform,
            "pkg_name": pkg_name,
            "id": advisory_id,
            "src": source,
        },
    }
    assert mock_query.await_count == 1
    assert mock_batch_delete_item.call_args.kwargs == {
        "keys": (PrimaryKey("pk_value", "sk_value"),),
        "table": TABLE,
    }
    assert mock_print.call_args.args == (
        f"Removed ( {platform}#{pkg_name}  {advisory_id}#{source} )",
    )


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_remove(
    mocker: MockerFixture,
    mock_builtins_print: Mock,
) -> None:
    platform = "npm"
    pkg_name = "package1"
    advisory_id = "ADV-001"
    source = "SOURCE"
    module_remove = import_module("db_model.advisories.remove")
    mocker.patch.object(module_remove, "TABLE", TABLE)
    mock_build_key = mocker.patch(
        "db_model.advisories.remove.keys.build_key",
        return_value=PRIMARY_KEY_TEST,
    )
    mock_delete_item = mocker.patch(
        "db_model.advisories.remove.operations.delete_item"
    )
    await remove(
        platform=platform,
        pkg_name=pkg_name,
        advisory_id=advisory_id,
        source=source,
    )
    assert mock_build_key.call_args.kwargs == {
        "facet": TABLE.facets["advisories"],
        "values": {
            "platform": platform,
            "pkg_name": pkg_name,
            "id": advisory_id,
            "src": source,
        },
    }
    assert mock_delete_item.call_args.kwargs == {
        "key": mock_build_key.return_value,
        "table": TABLE,
    }
    assert mock_builtins_print.call_args.args == (
        f"Removed ( {platform}#{pkg_name}  {advisory_id}#{source} )",
    )
