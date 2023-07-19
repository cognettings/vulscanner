from batch.dal import (
    delete_action,
)
from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
)
import pytest
from pytest_mock import (
    MockerFixture,
)
from roots import (
    domain as roots_domain,
    utils as roots_utils,
)
from roots.utils import (
    update_root_cloning_status,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_ssh_ok(mocker: MockerFixture) -> None:
    mocker.patch.object(roots_utils, "is_in_s3", return_value=False)
    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "6160f0cb-4b66-515b-4fc6-738282f535af")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    assert result.success
    # restore db state
    if result.dynamo_pk:
        await delete_action(dynamodb_pk=result.dynamo_pk)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_https_ok(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(roots_utils, "is_in_s3", return_value=False)
    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "7271f1cb-5b77-626b-5fc7-849393f646az")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    assert result.success
    # restore db state
    if result.dynamo_pk:
        await delete_action(dynamodb_pk=result.dynamo_pk)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_https_same_commit(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(roots_utils, "is_in_s3", return_value=True)
    loaders = get_new_context()
    await update_root_cloning_status(
        loaders,
        "group1",
        "7271f1cb-5b77-626b-5fc7-849393f646az",
        GitCloningStatus.OK,
        "Success",
        "63afdb8d9cc5230a0137593d20a2fd2c4c73b92b",
    )
    loaders.root.clear_all()
    root_1 = await loaders.root.load(
        RootRequest("group1", "7271f1cb-5b77-626b-5fc7-849393f646az")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_real_ssh_same_commit(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(roots_utils, "is_in_s3", return_value=True)
    loaders = get_new_context()
    await update_root_cloning_status(
        loaders,
        "group1",
        "6160f0cb-4b66-515b-4fc6-738282f535af",
        GitCloningStatus.OK,
        "Success",
        "63afdb8d9cc5230a0137593d20a2fd2c4c73b92b",
    )
    loaders.root.clear_all()
    root_1 = await loaders.root.load(
        RootRequest("group1", "6160f0cb-4b66-515b-4fc6-738282f535af")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert result is None


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_no_creds(mocker: MockerFixture) -> None:
    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "5059f0cb-4b55-404b-3fc5-627171f424af")
    )
    assert isinstance(root_1, GitRoot)
    mocker.patch.object(roots_utils, "is_in_s3", return_value=False)

    assert (
        await roots_domain.queue_sync_git_roots(
            loaders=loaders,
            roots=(root_1,),
            group_name="group1",
        )
        is None
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_no_queue(mocker: MockerFixture) -> None:
    mocker.patch.object(roots_utils, "is_in_s3", return_value=False)

    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert not result
    loaders.root.clear_all()
    root = await loaders.root.load(
        RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )
    assert isinstance(root, GitRoot)
    assert root.cloning.status == GitCloningStatus.FAILED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_cloning(mocker: MockerFixture) -> None:
    mocker.patch.object(roots_utils, "is_in_s3", return_value=False)
    mocker.patch.object(
        roots_utils,
        "ls_remote",
        return_value="904d294729ad03fd2dadbb89b920389458e53a61c",
    )
    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    loaders.root.clear_all()
    root = await loaders.root.load(
        RootRequest("group1", "88637616-41d4-4242-854a-db8ff7fe1ab6")
    )
    assert isinstance(root, GitRoot)
    assert root.cloning.status == GitCloningStatus.QUEUED


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_with_same_commit_in_s3(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        roots_utils,
        "ls_remote",
        return_value="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
    )
    mocker.patch.object(
        roots_utils,
        "is_in_s3",
        return_value=True,
    )

    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert not result
    loaders.root.clear_all()
    root = await loaders.root.load(
        RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert isinstance(root, GitRoot)
    assert root.cloning.status == GitCloningStatus.OK


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("batch")
async def test_queue_sync_git_roots_with_same_commit_not_in_s3(
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        roots_utils,
        "ls_remote",
        return_value="6d2059f5d5b3954feb65fcbc5a368e8ef9964b62",
    )
    mocker.patch.object(
        roots_utils,
        "is_in_s3",
        return_value=False,
    )

    loaders = get_new_context()
    root_1 = await loaders.root.load(
        RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert isinstance(root_1, GitRoot)

    result = await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(root_1,),
        group_name="group1",
    )
    assert result
    loaders.root.clear_all()
    root = await loaders.root.load(
        RootRequest("group1", "2159f8cb-3b55-404b-8fc5-627171f424ax")
    )
    assert isinstance(root, GitRoot)
    assert root.cloning.status == GitCloningStatus.QUEUED
