from custom_utils import (
    datetime as datetime_utils,
)
from dataloaders import (
    get_new_context,
)
from datetime import (
    date,
    datetime,
)
import pytest
from schedulers.numerator_report_digest import (
    _common_generate_count_report,
    _generate_fields,
    _generate_group_fields,
    _send_mail_report,
    _validate_date,
    get_percent,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_get_percent() -> None:
    assert get_percent(0, 10) == "+0%"
    assert get_percent(10, 0) == "-"
    # FP: local testing
    assert get_percent("0", 10) == "-"  # type: ignore  # NOSONAR
    assert get_percent(-10, 10) == "-100%"
    assert get_percent(0.55, 10) == "+6%"
    assert get_percent(2, 3) == "+67%"
    assert get_percent(3, 2) == "+150%"
    assert get_percent(-2, 3) == "-67%"
    assert get_percent(-3, 2) == "-150%"


def test_validate_date() -> None:
    report_date: date = datetime_utils.get_now_minus_delta(days=1).date()
    in_range_date: date = datetime_utils.get_now_minus_delta(days=2).date()
    in_range_date2: date = datetime_utils.get_now_minus_delta(days=9).date()
    assert _validate_date(report_date, 1, 0)
    assert _validate_date(in_range_date, 2, 1)
    assert _validate_date(in_range_date, 9, 1)
    assert _validate_date(in_range_date2, 9, 1)


def test_validate_date_fail() -> None:
    actual_date: date = datetime_utils.get_now().date()
    not_in_range_date: date = datetime_utils.get_now_minus_delta(days=2).date()
    not_in_range_date2: date = datetime_utils.get_now_minus_delta(
        days=10
    ).date()
    assert not _validate_date(actual_date, 1, 0)
    assert not _validate_date(actual_date, 9, 2)
    assert not _validate_date(not_in_range_date, 1, 0)
    assert not _validate_date(not_in_range_date, 9, 2)
    assert not _validate_date(not_in_range_date2, 9, 0)
    assert not _validate_date(not_in_range_date2, 20, 10)


def test_common_generate_count_report() -> None:
    date_days = 3 if datetime_utils.get_now().weekday() == 0 else 1
    user_email: str = "test@test.com"
    content: dict[str, Any] = {user_email: _generate_fields()}
    content[user_email]["groups"] = {
        "unittesting": _generate_group_fields(),
        "test_group": _generate_group_fields(),
    }
    fields: list[str] = [
        "verified_inputs",
        "verified_inputs",
        "verified_inputs",
        "verified_ports",
        "verified_ports",
        "enumerated_inputs",
        "enumerated_ports",
        "enumerated_ports",
        "released",
        "submitted",
    ]
    groups: list[str] = [
        "unittesting",
        "unittesting",
        "test_group",
        "test_group",
        "unittesting",
        "unittesting",
        "test_group",
        "unittesting",
        "test_group",
        "test_group",
        "test_group",
    ]

    for group, field in zip(groups, fields):
        _common_generate_count_report(
            content=content,
            date_range=date_days,
            date_report=datetime_utils.get_now_minus_delta(days=date_days),
            field=field,
            group=group,
            user_email=user_email,
            allowed_users=["test@test.com"],
        )

    assert content[user_email]["verified_inputs"]["count"]["today"] == 3
    assert content[user_email]["enumerated_inputs"]["count"]["today"] == 1
    assert content[user_email]["released"]["count"]["today"] == 1
    assert content[user_email]["submitted"]["count"]["today"] == 1
    assert (
        content[user_email]["groups"]["unittesting"]["enumerated_inputs"] == 1
    )
    assert (
        content[user_email]["groups"]["unittesting"]["enumerated_ports"] == 1
    )
    assert content[user_email]["groups"]["unittesting"]["verified_inputs"] == 2
    assert content[user_email]["groups"]["unittesting"]["verified_ports"] == 1
    assert (
        content[user_email]["groups"]["test_group"]["enumerated_inputs"] == 0
    )
    assert content[user_email]["groups"]["test_group"]["enumerated_ports"] == 1
    assert content[user_email]["groups"]["test_group"]["verified_inputs"] == 1
    assert content[user_email]["groups"]["test_group"]["verified_ports"] == 1
    assert content[user_email]["groups"]["test_group"]["released"] == 1
    assert content[user_email]["groups"]["test_group"]["submitted"] == 1
    past_days = 4 if datetime_utils.get_now().weekday() == 1 else date_days + 1
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_inputs",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_inputs",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    assert content[user_email]["verified_inputs"]["count"]["past_day"] == 2
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_ports",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    _common_generate_count_report(
        content=content,
        date_range=date_days,
        date_report=datetime_utils.get_now_minus_delta(days=past_days),
        field="verified_ports",
        group="test_group",
        user_email=user_email,
        allowed_users=["test@test.com"],
    )
    assert content[user_email]["verified_ports"]["count"]["past_day"] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "content",
    ],
    [
        [
            {
                "enumerated_inputs": {
                    "count": {
                        "past_day": 4,
                        "today": 10,
                    }
                },
                "verified_inputs": {
                    "count": {
                        "past_day": 3,
                        "today": 5,
                    }
                },
                "enumerated_ports": {
                    "count": {
                        "past_day": 4,
                        "today": 10,
                    }
                },
                "verified_ports": {
                    "count": {
                        "past_day": 3,
                        "today": 5,
                    }
                },
                "loc": {
                    "count": {
                        "past_day": 4,
                        "today": 5,
                    }
                },
                "reattacked": {
                    "count": {
                        "past_day": 3,
                        "today": 2,
                    }
                },
                "released": {
                    "count": {
                        "past_day": 1,
                        "today": 2,
                    }
                },
                "submitted": {
                    "count": {
                        "past_day": 2,
                        "today": 3,
                    }
                },
                "max_cvss": 0.0,
                "groups": {
                    "unittesting": {
                        "verified_inputs": 6,
                        "verified_ports": 6,
                        "enumerated_inputs": 3,
                        "enumerated_ports": 3,
                        "loc": 0,
                    },
                    "test_group": {
                        "verified_inputs": 4,
                        "verified_ports": 4,
                        "enumerated_inputs": 2,
                        "enumerated_ports": 2,
                        "loc": 0,
                    },
                },
            },
        ],
    ],
)
async def test_send_mail_numerator_report(
    content: dict[str, Any],
) -> None:
    with mock.patch(
        "schedulers.numerator_report_digest.mail_numerator_report",
        new_callable=mock.AsyncMock,
    ) as mock_mail_numerator_report:
        mock_mail_numerator_report.return_value = True
        await _send_mail_report(
            loaders=get_new_context(),
            content=content,
            report_date=datetime.fromisoformat(
                "2022-07-08T06:00:00+00:00"
            ).date(),
            responsible="integratesmanager@gmail.com",
        )
    assert mock_mail_numerator_report.called is True
