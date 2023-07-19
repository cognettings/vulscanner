from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers import (
    newsletter,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("newsletter_notification")
@freeze_time("2022-11-11T15:58:31.280182")
async def test_newsletter_notification(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_spy = mocker.spy(newsletter, "mail_newsletter")

    await newsletter.main()

    assert mail_spy.await_count == 1
    mail_spy.assert_any_call(
        loaders=mock.ANY,
        context={},
        email_to=["johndoe@fluidattacks.com"],
        email_cc=[],
    )
