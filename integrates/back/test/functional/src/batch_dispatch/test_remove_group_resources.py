from batch.enums import (
    Action,
    IntegratesBatchQueue,
)
from batch.types import (
    BatchProcessing,
)
from batch_dispatch.remove_group_resources import (
    remove_group_resources,
)
from custom_utils.datetime import (
    get_as_epoch,
    get_now,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch_dispatch")
async def test_remove_group_resources(
    populate: bool, generic_data: dict
) -> None:
    assert populate
    group_name = "group1"
    loaders: Dataloaders = get_new_context()
    assert await loaders.group.load(group_name)
    assert await loaders.group_roots.load(group_name)
    assert await loaders.group_stakeholders_access.load(group_name)
    action = BatchProcessing(
        action_name=Action.REMOVE_GROUP_RESOURCES.value,
        entity="group1",
        subject=generic_data["global_vars"]["admin_email"],
        time=str(get_as_epoch(get_now())),
        additional_info="validate_pending_actions: testing",
        batch_job_id=None,
        queue=IntegratesBatchQueue.SMALL.value,
        key="2",
    )
    await remove_group_resources(item=action)
    loaders.group.clear_all()
    loaders.group_roots.clear_all()
    loaders.group_stakeholders_access.clear_all()
    assert not await loaders.group.load(group_name)
    assert not await loaders.group_stakeholders_access.load(group_name)
    assert not await loaders.group_roots.load(group_name)
