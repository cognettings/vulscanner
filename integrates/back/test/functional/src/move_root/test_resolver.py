# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
)
from batch_dispatch import (
    move_root,
)
from custom_exceptions import (
    InvalidParameter,
)
from dataloaders import (
    get_new_context,
)
from db_model.event_comments.types import (
    EventCommentsRequest,
)
from db_model.events.enums import (
    EventSolutionReason,
    EventStateStatus,
)
from db_model.events.types import (
    GroupEventsRequest,
)
from db_model.roots.types import (
    GitRoot,
    RootEnvironmentSecretsRequest,
)
import pytest
from typing import (
    Any,
)


async def resolve(
    *,
    group_name: str,
    root_id: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        query {{
            root(groupName: "{group_name}", rootId: "{root_id}") {{
                ... on GitRoot {{
                    state
                }}
                ... on IPRoot {{
                    state
                }}
                ... on URLRoot {{
                    state
                }}
            }}
        }}
    """
    data = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


async def mutate(
    *,
    root_id: str,
    source_group_name: str,
    target_group_name: str,
    user: str,
) -> dict[str, Any]:
    query: str = f"""
        mutation {{
            moveRoot(
                groupName: "{source_group_name}",
                id: "{root_id}",
                targetGroupName: "{target_group_name}"
            ) {{
                success
            }}
        }}
    """
    data = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
async def test_should_mutate_successfully(populate: bool) -> None:
    assert populate
    result = await resolve(
        group_name="kibi",
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        user="test@fluidattacks.com",
    )
    batch_actions = await batch_dal.get_actions()
    assert result["data"]["root"]["state"] == "ACTIVE"
    assert len(batch_actions) == 0

    result = await mutate(
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        source_group_name="kibi",
        target_group_name="kuri",
        user="test@fluidattacks.com",
    )
    assert "errors" not in result
    assert "success" in result["data"]["moveRoot"]
    assert result["data"]["moveRoot"]["success"]

    result = await resolve(
        group_name="kibi",
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        user="test@fluidattacks.com",
    )
    assert result["data"]["root"]["state"] == "INACTIVE"
    batch_actions = await batch_dal.get_actions()
    assert len(batch_actions) == 3

    actions_by_name = {
        Action[action.action_name.upper()]: action for action in batch_actions
    }
    assert Action.MOVE_ROOT in actions_by_name
    assert Action.REFRESH_TOE_LINES in actions_by_name
    assert Action.REFRESH_TOE_INPUTS in actions_by_name

    await move_root.move_root(item=actions_by_name[Action.MOVE_ROOT])

    loaders = get_new_context()
    target_root = next(
        (
            root
            for root in await loaders.group_roots.load("kuri")
            if root.state.nickname == "test"
        ),
        None,
    )
    assert isinstance(target_root, GitRoot)
    source_events = await loaders.group_events.load(
        GroupEventsRequest(
            group_name="kibi",
        )
    )
    assert len(source_events) == 2
    assert source_events[0].state.status == EventStateStatus.SOLVED
    assert (
        source_events[0].state.reason
        == EventSolutionReason.MOVED_TO_ANOTHER_GROUP
    )
    assert source_events[0].state.other is None
    target_events = await loaders.group_events.load(
        GroupEventsRequest(
            group_name="kuri",
        )
    )
    assert len(target_events) == 1
    assert target_events[0].state.status == EventStateStatus.CREATED
    target_event_comments = await loaders.event_comments.load(
        EventCommentsRequest(
            event_id=target_events[0].id,
            group_name=target_events[0].group_name,
        )
    )
    assert len(target_event_comments) == 1
    assert target_event_comments[0].id == "43455343453"
    assert target_event_comments[0].parent_id == "0"
    target_root_environment_urls = await loaders.root_environment_urls.load(
        target_root.id
    )
    assert len(target_root_environment_urls) == 1
    assert target_root_environment_urls[0].url == "https://test-active.com"
    target_environment_secrets = await loaders.environment_secrets.load(
        RootEnvironmentSecretsRequest(
            group_name="kuri", url_id=target_root_environment_urls[0].id
        )
    )
    assert len(target_environment_secrets) == 2
    assert target_environment_secrets[0].key == "Key1"
    assert target_environment_secrets[0].value == "Value1"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
@pytest.mark.parametrize(
    ("user", "root_id", "group_name"),
    (
        (
            "test@fluidattacks.com",
            "44db9bee-c97d-4161-98c6-f124d7dc9a41",
            "kibi",
        ),
    ),
)
async def test_should_move_ip_root(
    populate: bool, user: str, root_id: str, group_name: str
) -> None:
    assert populate
    result = await resolve(
        group_name=group_name,
        root_id=root_id,
        user=user,
    )
    batch_actions = await batch_dal.get_actions()
    assert result["data"]["root"]["state"] == "ACTIVE"
    assert len(batch_actions) == 4

    result = await mutate(
        root_id=root_id,
        source_group_name=group_name,
        target_group_name="kuri",
        user=user,
    )
    assert "errors" not in result
    assert "success" in result["data"]["moveRoot"]
    assert result["data"]["moveRoot"]["success"]

    result = await resolve(
        group_name=group_name,
        root_id=root_id,
        user=user,
    )
    assert result["data"]["root"]["state"] == "INACTIVE"
    batch_actions = await batch_dal.get_actions()
    assert len(batch_actions) == 6

    actions_by_name = {
        Action[action.action_name.upper()]: action for action in batch_actions
    }
    assert Action.MOVE_ROOT in actions_by_name
    assert Action.REFRESH_TOE_LINES in actions_by_name
    assert Action.REFRESH_TOE_INPUTS in actions_by_name

    await move_root.move_root(item=actions_by_name[Action.MOVE_ROOT])


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("move_root")
@pytest.mark.parametrize(
    ("root_id", "source_group_name", "target_group_name"),
    (
        # Inactive root
        (
            "8a62109b-316a-4a88-a1f1-767b80383864",
            "kibi",
            "kuri",
        ),
        # Same group
        (
            "88637616-41d4-4242-854a-db8ff7fe1ab6",
            "kibi",
            "kibi",
        ),
        # Target group outside the organization
        (
            "88637616-41d4-4242-854a-db8ff7fe1ab6",
            "kibi",
            "kurau",
        ),
        # Groups with different services
        (
            "88637616-41d4-4242-854a-db8ff7fe1ab6",
            "kibi",
            "udon",
        ),
    ),
)
async def test_should_trigger_validations(
    populate: bool,
    root_id: str,
    source_group_name: str,
    target_group_name: str,
) -> None:
    assert populate
    result = await mutate(
        root_id=root_id,
        source_group_name=source_group_name,
        target_group_name=target_group_name,
        user="test@fluidattacks.com",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == InvalidParameter().args[0]
