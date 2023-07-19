from custom_exceptions import (
    CouldNotVerifyStakeholder,
    InvalidMobileNumber,
)
import pytest
from typing import (
    NamedTuple,
)
from unittest import (
    mock,
)
from verify.operations import (
    check_verification,
    get_country_code,
    start_verification,
    validate_mobile,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_country_code() -> None:
    class MockedTwilioObject(NamedTuple):
        caller_name: str
        carrier: dict
        country_code: str
        national_format: str
        phone_number: str
        add_ons: str
        url: str

    test_phone_number = "+15108675310"
    test_result = await get_country_code(test_phone_number)
    assert test_result == ""
    mocked_response = MockedTwilioObject(
        caller_name="null",
        carrier={
            "error_code": "null",
            "mobile_country_code": "310",
            "mobile_network_code": "456",
            "name": "verizon",
            "type": "mobile",
        },
        country_code="US",
        national_format="(510) 867-5310",
        phone_number="+15108675310",
        add_ons="null",
        url="https://lookups.twilio.com/v1/PhoneNumbers/+15108675310",
    )
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        with mock.patch("verify.operations.client"):
            with mock.patch(
                "verify.operations.client.lookups.v1.phone_numbers"
            ) as mock_twilio:
                mock_twilio.return_value.fetch.return_value = mocked_response
                test_result = await get_country_code("+15108675310")
        with pytest.raises(InvalidMobileNumber):
            await get_country_code("0000")
    assert mock_twilio.called is True
    assert test_result == "US"


async def test_check_verification() -> None:
    class MockedTwilioObject(NamedTuple):
        sid: str
        service_sid: str
        account_sid: str
        to: str
        channel: str
        status: str
        valid: bool
        amount: str
        payee: str
        sna_attempts_error_codes: list
        date_created: str
        date_updated: str

    test_phone_number = "12345678"
    test_code = "US"
    await check_verification(recipient=test_phone_number, code=test_code)
    mocked_response = MockedTwilioObject(
        sid="VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        service_sid="VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        account_sid="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        to="+15017122661",
        channel="sms",
        status="approved",
        valid=True,
        amount="test",
        payee="test",
        sna_attempts_error_codes=[],
        date_created="2015-07-30T20:00:00Z",
        date_updated="2015-07-30T20:00:00Z",
    )
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        with mock.patch("verify.operations.client"):
            with mock.patch(
                "verify.operations.client.verify.services"
            ) as mocked:
                mocked.return_value.verification_checks.create.return_value = (
                    mocked_response
                )
                await check_verification(recipient="+15017122661", code="US")

        with pytest.raises(CouldNotVerifyStakeholder):
            await check_verification(recipient="", code=test_code)
    assert mocked.called is True


async def test_start_verification() -> None:
    class MockedTwilioObject(NamedTuple):
        sid: str
        service_sid: str
        account_sid: str
        to: str
        channel: str
        status: str
        valid: bool
        date_created: str
        date_updated: str
        lookup: dict
        amount: str
        payee: str
        send_code_attempts: list
        sna: str
        url: str

    test_phone_number = "12345678"
    await start_verification(phone_number=test_phone_number)
    mocked_response = MockedTwilioObject(
        sid="VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        service_sid="VAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        account_sid="ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        to="+15017122661",
        channel="sms",
        status="pending",
        valid=False,
        date_created="2015-07-30T20:00:00Z",
        date_updated="2015-07-30T20:00:00Z",
        lookup=dict(test_key="test_value"),
        amount="0",
        payee="test",
        send_code_attempts=[
            dict(
                time="2015-07-30T20:00:00Z",
                channel="SMS",
                attempt_sid="VLXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            ),
        ],
        sna="test",
        url="""https://verify.twilio.com/v2/Services/VAXXXXXXXXXXXXXXXXXXXXXX
            XXXXXXXXXX/Verifications/VEXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX""",
    )
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        with mock.patch("verify.operations.client"):
            with mock.patch(
                "verify.operations.client.verify.services"
            ) as mock_twilio:
                mock_twilio.return_value.verifications.create.return_value = (
                    mocked_response
                )
                await start_verification(phone_number="+15017122661")
    assert mock_twilio.called is True


async def test_validate_mobile() -> None:
    class MockedTwilioObject(NamedTuple):
        caller_name: str
        carrier: dict
        country_code: str
        national_format: str
        phone_number: str
        add_ons: str
        url: str

    test_phone_number = "12345678"
    await validate_mobile(test_phone_number)
    mocked_response = MockedTwilioObject(
        caller_name="null",
        carrier={
            "error_code": "null",
            "mobile_country_code": "310",
            "mobile_network_code": "456",
            "name": "verizon",
            "type": "mobile",
        },
        country_code="US",
        national_format="(510) 867-5310",
        phone_number="+15108675310",
        add_ons="null",
        url="https://lookups.twilio.com/v1/PhoneNumbers/+15108675310",
    )
    with mock.patch("verify.operations.FI_ENVIRONMENT", "production"):
        with mock.patch("verify.operations.client"):
            with mock.patch(
                "verify.operations.client.lookups.v1.phone_numbers"
            ) as mock_twilio:
                mock_twilio.return_value.fetch.return_value = mocked_response
                await validate_mobile("+15108675310")
    assert mock_twilio.called is True
