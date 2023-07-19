import json
import pytest
from tap_zoho_crm._cli._decode import (
    decode_zoho_creds,
)
from tap_zoho_crm.api.auth import (
    Credentials,
)
import tempfile


def test_decode_zoho_creds() -> None:
    with tempfile.TemporaryFile("w+") as file:
        test_file_data = {
            "client_id": "client_1",
            "client_secret": "the_secret",
            "refresh_token": "super_rtoken",
            "scopes": ["s1", "s2"],
        }
        file.write(json.dumps(test_file_data))
        file.seek(0)
        result = decode_zoho_creds(file).unwrap()
        expected = Credentials(
            "client_1", "the_secret", "super_rtoken", frozenset(["s1", "s2"])
        )
        assert result == expected


@pytest.mark.skip(
    reason="need manual intervention to retrieve the access code"
)
def test_generate_refresh_token() -> None:
    # non testable
    pass


@pytest.mark.skip(
    reason="need real credentials and can invalidate other tokens"
)
def test_generate_token() -> None:
    # non testable
    pass
