# pylint: disable=invalid-name,import-error
"""
Add the group name in every event comment.

Start Time:    2023-07-07 at 19:31:28 UTC
Finalization Time: 2023-07-07 at 19:41:11 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    TABLE,
)
from db_model.event_comments.constants import (
    NEW_EVENT_COMMENT_FACET,
)
from db_model.event_comments.types import (
    EventComment,
    EventCommentsRequest,
)
from db_model.events.types import (
    GroupEventsRequest,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
from organizations import (
    domain as orgs_domain,
)
import time


async def _get_event_comments(
    loaders: Dataloaders, event_id: str, group_name: str
) -> list[EventComment]:
    return await loaders.event_comments.load(
        EventCommentsRequest(event_id=event_id, group_name=group_name)
    )


async def process_comment(comment: EventComment, group_name: str) -> None:
    key_structure = TABLE.primary_key
    new_primary_key = keys.build_key(
        facet=NEW_EVENT_COMMENT_FACET,
        values={
            "event_id": comment.event_id,
            "group_name": group_name,
            "id": comment.id,
        },
    )
    item = {"group_name": group_name}
    await operations.update_item(
        condition_expression=Attr(key_structure.partition_key).exists(),
        item=item,
        key=new_primary_key,
        table=TABLE,
    )


async def process_group(
    loaders: Dataloaders,
    group_name: str,
) -> None:
    events = await loaders.group_events.load(
        GroupEventsRequest(group_name=group_name)
    )
    group_event_comments = list(
        chain.from_iterable(
            await collect(
                tuple(
                    _get_event_comments(
                        loaders=loaders,
                        event_id=event.id,
                        group_name=group_name,
                    )
                    for event in events
                ),
                workers=5,
            )
        )
    )
    await collect(
        tuple(
            process_comment(comment, group_name)
            for comment in group_event_comments
        ),
        workers=5,
    )
    print(f"Group processed {group_name}")


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_group_names = sorted(
        await orgs_domain.get_all_group_names(loaders=loaders)
    )
    count = 0
    print("all_group_names", len(all_group_names))
    for group_name in all_group_names:
        count += 1
        print("group", group_name, count)
        await process_group(loaders, group_name)


if __name__ == "__main__":
    execution_time = time.strftime("Start Time:    %Y-%m-%d at %H:%M:%S UTC")
    print(execution_time)
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
