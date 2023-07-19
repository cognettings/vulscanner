from datetime import (
    datetime,
)
from freezegun import (
    freeze_time,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from schedulers import (
    reviewer_progress_report,
)
from unittest import (
    mock,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("reviewer_progress_report")
@freeze_time("2018-04-09T05:45:15+00:00")
async def test_reviewer_progress_report(
    *, populate: bool, mocker: MockerFixture
) -> None:
    assert populate
    mail_spy = mocker.spy(
        reviewer_progress_report, "mail_reviewer_progress_report"
    )

    await reviewer_progress_report.main()

    mail_spy.assert_called_once_with(
        context={
            "global_info": {
                "oldest_rejected": {
                    "datetime": datetime.fromisoformat(
                        "2018-04-08T05:45:15+00:00"
                    ),
                    "finding_id": "3c475384-834c-47b0-ac71-a41a022e401c",
                    "finding_title": "001. SQL injection - C Sharp SQL API",
                    "group_name": "group1",
                    "id": "be09edb7-cd5c-47ed-bee4-97c645acdce10",
                    "org_name": "orgtest",
                    "specific": "9999",
                    "where": "192.168.1.20",
                },
                "rejected_count": 2,
                "submitted_count": 2,
            },
            "mailto": "reviewer@fluidattacks.com",
            "name": "reviewer",
            "responsible": "reviewer@fluidattacks.com",
            "stakeholder_info": {
                "rejected_count": 2,
                "vulnerable_count": 1,
            },
            "year": "2018",
        },
        loaders=mock.ANY,
        email_to=["reviewer@fluidattacks.com"],
        email_cc=["cos.mail@integrates.test", "cto.mail@integrates.test"],
        report_date=datetime.fromisoformat("2018-04-08T05:00:00+00:00").date(),
        responsible="reviewer@fluidattacks.com",
    )
