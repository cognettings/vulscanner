from collections.abc import (
    Callable,
)
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from db_model.types import (
    Connection,
    Edge,
    PoliciesToUpdate,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Index,
    Item,
    QueryResponse,
    Table,
)
from dynamodb.utils import (
    get_cursor,
)
from typing import (
    Any,
    TypeVar,
)

T = TypeVar("T")


def adjust_historic_dates(historic: tuple[Any, ...]) -> tuple[Any, ...]:
    """
    Ensure dates are not the same and in ascending order.
    Also add a minimum 1 second offset among them.
    """
    if not historic:
        return tuple()
    new_historic = [historic[0]]
    base_date: datetime = historic[0].modified_date
    for entry in historic[1:]:
        base_date = get_datetime_with_offset(base_date, entry.modified_date)
        new_historic.append(entry._replace(modified_date=base_date))

    return tuple(new_historic)


def get_as_utc_iso_format(date: datetime) -> str:
    return date.astimezone(tz=timezone.utc).isoformat()


def get_min_iso_date(date: datetime) -> datetime:
    return datetime.combine(
        date.astimezone(tz=timezone.utc),
        datetime.min.time(),
    )


def get_first_day_iso_date() -> datetime:
    now = get_min_iso_date(datetime.now(tz=timezone.utc))

    return now - timedelta(days=(now.isoweekday() - 1) % 7)


def get_datetime_with_offset(
    base_iso8601: datetime, target_iso8601: datetime, offset: int = 1
) -> datetime:
    """Guarantee at least n seconds separation between dates."""
    return max(base_iso8601 + timedelta(seconds=offset), target_iso8601)


def format_policies_to_update(
    policies_data: dict[str, Any],
) -> PoliciesToUpdate:
    return PoliciesToUpdate(
        inactivity_period=int(policies_data["inactivity_period"])
        if policies_data.get("inactivity_period") is not None
        else None,
        max_acceptance_days=int(policies_data["max_acceptance_days"])
        if policies_data.get("max_acceptance_days") is not None
        else None,
        max_acceptance_severity=Decimal(
            policies_data["max_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("max_acceptance_severity") is not None
        else None,
        max_number_acceptances=int(policies_data["max_number_acceptances"])
        if policies_data.get("max_number_acceptances") is not None
        else None,
        min_acceptance_severity=Decimal(
            policies_data["min_acceptance_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("min_acceptance_severity") is not None
        else None,
        min_breaking_severity=Decimal(
            policies_data["min_breaking_severity"]
        ).quantize(Decimal("0.1"))
        if policies_data.get("min_breaking_severity") is not None
        else None,
        vulnerability_grace_period=int(
            policies_data["vulnerability_grace_period"]
        )
        if policies_data.get("vulnerability_grace_period") is not None
        else None,
    )


def serialize(object_: object) -> Any:
    if isinstance(object_, set):
        return list(object_)
    if isinstance(object_, datetime):
        return object_.astimezone(tz=timezone.utc).isoformat()
    if isinstance(object_, float):
        return Decimal(str(object_))

    return object_


def format_edge(
    index: Index | None,
    item: Item,
    formatter: Callable[[Item], T],
    table: Table,
) -> Edge[T]:
    return Edge[T](node=formatter(item), cursor=get_cursor(index, item, table))


def format_connection(
    *,
    index: Index | None,
    formatter: Callable[[Item], T],
    response: QueryResponse,
    table: Table,
) -> Connection[T]:
    return Connection[T](
        edges=tuple(
            format_edge(index, item, formatter, table)
            for item in response.items
        ),
        page_info=response.page_info,
    )
