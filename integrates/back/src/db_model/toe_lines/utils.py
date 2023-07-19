from .types import (
    SortsSuggestion,
    ToeLines,
    ToeLinesEdge,
    ToeLinesState,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb.types import (
    Index,
    Item,
    PrimaryKey,
    Table,
)
from dynamodb.utils import (
    get_cursor,
)


def format_toe_lines_sorts_suggestions(
    suggestions: list[Item],
) -> list[SortsSuggestion]:
    return [
        SortsSuggestion(
            finding_title=suggestion["finding_title"],
            probability=int(suggestion["probability"]),
        )
        for suggestion in suggestions
    ]


def format_toe_lines(item: Item) -> ToeLines:
    state_item: Item = item["state"]
    return ToeLines(
        filename=item["filename"],
        group_name=item["group_name"],
        root_id=item["root_id"],
        seen_first_time_by=item.get("seen_first_time_by"),
        state=ToeLinesState(
            attacked_at=datetime.fromisoformat(state_item["attacked_at"])
            if state_item.get("attacked_at")
            else None,
            attacked_by=state_item.get("attacked_by", ""),
            attacked_lines=int(state_item["attacked_lines"]),
            be_present=state_item["be_present"],
            be_present_until=datetime.fromisoformat(
                state_item["be_present_until"]
            )
            if state_item.get("be_present_until")
            else None,
            comments=state_item["comments"],
            first_attack_at=datetime.fromisoformat(
                state_item["first_attack_at"]
            )
            if state_item.get("first_attack_at")
            else None,
            has_vulnerabilities=state_item.get("has_vulnerabilities"),
            last_author=state_item["last_author"],
            last_commit=state_item["last_commit"],
            last_commit_date=datetime.fromisoformat(
                state_item.get("last_commit_date", item.get("modified_date"))
            ),
            loc=int(state_item["loc"]),
            modified_by=state_item["modified_by"],
            modified_date=datetime.fromisoformat(state_item["modified_date"]),
            seen_at=datetime.fromisoformat(state_item["seen_at"]),
            sorts_risk_level=int(state_item.get("sorts_risk_level", "-1")),
            sorts_priority_factor=int(
                state_item.get("sorts_priority_factor", "-1")
            ),
            sorts_risk_level_date=datetime.fromisoformat(
                state_item["sorts_risk_level_date"]
            )
            if state_item.get("sorts_risk_level_date")
            else None,
            sorts_suggestions=format_toe_lines_sorts_suggestions(
                state_item["sorts_suggestions"]
            )
            if state_item.get("sorts_suggestions")
            else None,
        ),
    )


def format_toe_lines_edge(
    index: Index | None,
    item: Item,
    table: Table,
) -> ToeLinesEdge:
    return ToeLinesEdge(
        node=format_toe_lines(item), cursor=get_cursor(index, item, table)
    )


def format_toe_lines_sorts_suggestions_item(
    suggestions: list[SortsSuggestion],
) -> list[Item]:
    return [
        {
            "finding_title": suggestion.finding_title,
            "probability": suggestion.probability,
        }
        for suggestion in suggestions
    ]


def format_toe_lines_item(
    primary_key: PrimaryKey,
    key_structure: PrimaryKey,
    toe_lines: ToeLines,
    gsi_2_index: Index | None = None,
    gsi_2_key: PrimaryKey | None = None,
) -> Item:
    toe_lines_item = {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        "filename": toe_lines.filename,
        "group_name": toe_lines.group_name,
        "root_id": toe_lines.root_id,
        "seen_first_time_by": toe_lines.seen_first_time_by,
        "state": {
            "attacked_at": get_as_utc_iso_format(toe_lines.state.attacked_at)
            if toe_lines.state.attacked_at
            else None,
            "attacked_by": toe_lines.state.attacked_by,
            "attacked_lines": toe_lines.state.attacked_lines,
            "be_present": toe_lines.state.be_present,
            "be_present_until": get_as_utc_iso_format(
                toe_lines.state.be_present_until
            )
            if toe_lines.state.be_present_until
            else None,
            "comments": toe_lines.state.comments,
            "first_attack_at": get_as_utc_iso_format(
                toe_lines.state.first_attack_at
            )
            if toe_lines.state.first_attack_at
            else None,
            "has_vulnerabilities": toe_lines.state.has_vulnerabilities,
            "last_author": toe_lines.state.last_author,
            "last_commit": toe_lines.state.last_commit,
            "last_commit_date": get_as_utc_iso_format(
                toe_lines.state.last_commit_date
            ),
            "loc": toe_lines.state.loc,
            "modified_by": toe_lines.state.modified_by,
            "modified_date": get_as_utc_iso_format(
                toe_lines.state.modified_date
            ),
            "seen_at": get_as_utc_iso_format(toe_lines.state.seen_at),
            "sorts_risk_level": toe_lines.state.sorts_risk_level,
            "sorts_priority_factor": toe_lines.state.sorts_priority_factor,
            "sorts_risk_level_date": get_as_utc_iso_format(
                toe_lines.state.sorts_risk_level_date
            )
            if toe_lines.state.sorts_risk_level_date
            else None,
            "sorts_suggestions": format_toe_lines_sorts_suggestions_item(
                toe_lines.state.sorts_suggestions
            )
            if toe_lines.state.sorts_suggestions
            else None,
        },
    }
    if gsi_2_index is not None and gsi_2_key is not None:
        toe_lines_item |= {
            gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
            gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        }
    return toe_lines_item
