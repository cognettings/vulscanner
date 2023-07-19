from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
import json
import pytest
from pytest_mock import (
    MockerFixture,
)
from s3.model.types import (
    Advisory,
)
from s3.operations import (
    download_advisories_dict,
    download_json_fileobj,
    upload_advisories,
    upload_object,
)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_upload_object(
    mocker: MockerFixture,
) -> None:
    s3_operations: str = "s3.operations"
    file_name: str = "file_name"
    dict_object: dict = {"key": "value"}
    bucket: str = "bucket"
    mocker.patch("builtins.print")
    put_object_mock = mocker.AsyncMock()
    get_s3_resource_mock = mocker.patch(
        f"{s3_operations}.get_s3_resource",
        return_value=mocker.AsyncMock(put_object=put_object_mock),
    )
    await upload_object(file_name, dict_object, bucket)
    assert get_s3_resource_mock.await_count == 1
    assert put_object_mock.await_count == 1
    assert put_object_mock.call_args.kwargs == {
        "Body": json.dumps(dict_object, indent=2),
        "Bucket": bucket,
        "Key": file_name,
    }


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_upload_object_error(
    mocker: MockerFixture,
) -> None:
    mocker.patch(
        "s3.operations.get_s3_resource",
        side_effect=ClientError({}, "message"),
    )
    with pytest.raises(UnavailabilityError):
        await upload_object("", {}, "")


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_download_json_fileobj(
    mocker: MockerFixture,
) -> None:
    s3_operations: str = "s3.operations"
    file_name: str = "file_name"
    bucket: str = "bucket"
    expected_dict = {"key": "value"}
    download_fileobj_mock = mocker.AsyncMock(
        side_effect=lambda _, __, fileobj: (
            fileobj.write(json.dumps(expected_dict).encode("utf-8"))
        )
    )
    get_s3_resource_mock = mocker.patch(
        f"{s3_operations}.get_s3_resource",
        return_value=mocker.AsyncMock(download_fileobj=download_fileobj_mock),
    )
    result: dict = await download_json_fileobj(bucket, file_name)
    assert get_s3_resource_mock.await_count == 1
    assert download_fileobj_mock.await_count == 1
    assert download_fileobj_mock.call_args.args == (
        bucket,
        file_name,
        mocker.ANY,
    )
    assert result == expected_dict


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_download_json_fileobj_error(
    mocker: MockerFixture,
) -> None:
    s3_operations: str = "s3.operations"
    file_name: str = "file_name"
    bucket: str = "bucket"
    value_error: Exception = ValueError("message")
    download_fileobj_mock = mocker.AsyncMock(side_effect=value_error)
    get_s3_resource_mock = mocker.patch(
        f"{s3_operations}.get_s3_resource",
        return_value=mocker.AsyncMock(download_fileobj=download_fileobj_mock),
    )
    log_blocking_mock = mocker.patch(f"{s3_operations}.log_blocking")
    await download_json_fileobj(bucket, file_name)
    assert get_s3_resource_mock.await_count == 1
    assert download_fileobj_mock.await_count == 1
    assert log_blocking_mock.call_args.args == ("error", "%s", value_error)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "to_storage, s3_advisories",
    [
        (
            (
                Advisory(
                    id="CVE-2021-0001",
                    package_name="package1",
                    package_manager="manager1",
                    vulnerable_version="version1",
                    source="source1",
                ),
                Advisory(
                    id="CVE-2021-0002",
                    package_name="package2",
                    package_manager="manager2",
                    vulnerable_version="version2",
                    source="source2",
                ),
            ),
            None,
        ),
        (
            (
                Advisory(
                    id="CVE-2021-0001",
                    package_name="package1",
                    package_manager="manager1",
                    vulnerable_version="version1",
                    source="source1",
                ),
            ),
            {},
        ),
    ],
)
async def test_upload_advisories(
    mocker: MockerFixture,
    to_storage: tuple[Advisory, ...],
    s3_advisories: dict | None,
) -> None:
    upload_object_mock = mocker.patch(
        "s3.operations.upload_object",
        return_value=mocker.AsyncMock(),
    )

    def expected_call_args_list() -> list:
        args_list = []
        for adv in to_storage:
            args_list.append(
                mocker.call(
                    bucket="skims.sca",
                    dict_object={
                        adv.package_name: {
                            adv.id: {
                                "vulnerable_version": adv.vulnerable_version,
                                "cvss": adv.severity,
                                "cwe_ids": adv.cwe_ids,
                            }
                        }
                    },
                    file_name=f"{adv.package_manager}.json",
                )
            )
        return args_list

    await upload_advisories(to_storage, s3_advisories)
    assert upload_object_mock.await_count == len(
        to_storage if s3_advisories is None else s3_advisories
    )
    assert upload_object_mock.call_args_list == expected_call_args_list()


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
async def test_upload_advisories_error(
    mocker: MockerFixture,
) -> None:
    log_blocking_mock = mocker.patch("s3.operations.log_blocking")
    mocker.patch(
        "s3.operations.upload_object",
        side_effect=UnavailabilityError(),
    )
    await upload_advisories((), {"key": "value"})
    assert isinstance(log_blocking_mock.call_args.args[2], UnavailabilityError)


@pytest.mark.skims_test_group("unittesting")
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dl_only_patches, needed_platforms",
    [
        (True, ("platform1", "platform2")),
        (False, ("platform1")),
    ],
)
async def test_download_advisories(
    mocker: MockerFixture,
    dl_only_patches: bool,
    needed_platforms: tuple[str, ...],
) -> None:
    patch: str = "_patch"
    download_json_fileobj_mock = mocker.patch(
        "s3.operations.download_json_fileobj",
        side_effect=lambda _, file_name: (
            {f"key{patch if patch in file_name else ''}": "value"}
        ),
    )
    s3_advisories, s3_patch_advisories = await download_advisories_dict(
        needed_platforms, dl_only_patches
    )

    def get_dicts_advs(s3_advs: str = "") -> dict[str, dict[str, str]]:
        return {plat: {f"key{s3_advs}": "value"} for plat in needed_platforms}

    assert s3_patch_advisories == get_dicts_advs(patch)
    if dl_only_patches:
        assert download_json_fileobj_mock.await_count == len(needed_platforms)
        assert s3_advisories == {}
    else:
        assert s3_advisories == get_dicts_advs()
        assert (
            download_json_fileobj_mock.await_count == len(needed_platforms) * 2
        )
