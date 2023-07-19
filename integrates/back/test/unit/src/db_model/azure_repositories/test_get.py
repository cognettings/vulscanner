from back.test.unit.src.utils import (
    get_module_at_test,
)
from db_model.azure_repositories.get import (
    _get_profile,
)
from msrest.exceptions import (
    ClientRequestError,
)
from unittest.mock import (
    MagicMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)


@patch(MODULE_AT_TEST + "Connection", new_callable=MagicMock)
def test_get_profile_raises_exception(
    mock_connec: MagicMock,
) -> None:
    def my_side_effect() -> None:
        raise ClientRequestError("error")

    mock_connec.return_value.clients_v6_0.get_profile_client.side_effect = (
        my_side_effect
    )
    base_url = "fluid.com"
    access_token = "token_test"

    assert not _get_profile(base_url=base_url, access_token=access_token)
