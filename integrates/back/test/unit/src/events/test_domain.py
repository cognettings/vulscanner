from back.test.unit.src.utils import (
    create_dummy_info,
    create_dummy_simple_session,
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
)
from custom_exceptions import (
    EventAlreadyClosed,
    InvalidEventSolvingReason,
    InvalidFileName,
    InvalidFileSize,
    InvalidFileType,
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.enums import (
    EventEvidenceId,
    EventSolutionReason,
)
from events.domain import (
    add_comment,
    add_event,
    remove_event,
    solve_event,
    update_evidence,
    validate_evidence,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import json
import os
import pytest
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["comment_data"],
    [
        [
            EventComment(
                event_id="538745942",
                group_name="group1",
                parent_id="0",
                creation_date=datetime.fromisoformat(
                    "2022-12-29 14:14:19.182591+00:00"
                ),
                content="comment test",
                id="1672323259183",
                email="integratesmanager@gmail.com",
                full_name="John Doe",
            ),
        ],
    ],
)
@patch(MODULE_AT_TEST + "event_comments_domain.add", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "_check_invalid_comment", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "get_event", new_callable=AsyncMock)
async def test_add_comment(
    mock_get_event: AsyncMock,
    mock__check_invalid_comment: AsyncMock,
    mock_event_comments_domain_add: AsyncMock,
    comment_data: EventComment,
    mocked_data_for_module: Any,
) -> None:
    mocks_setup_list: list[tuple[AsyncMock, str, list[Any]]] = [
        (
            mock_get_event,
            "get_event",
            [comment_data.event_id],
        ),
        (
            mock__check_invalid_comment,
            "_check_invalid_comment",
            [
                comment_data.content,
                comment_data.email,
                comment_data.parent_id,
                comment_data.event_id,
            ],
        ),
        (
            mock_event_comments_domain_add,
            "event_comments_domain.add",
            [comment_data],
        ),
    ]
    # Set up mocks' results using mocked_data_for_module fixture
    for mock_item in mocks_setup_list:
        mock, path, arguments = mock_item
        mock.return_value = mocked_data_for_module(
            mock_path=path,
            mock_args=arguments,
            module_at_test=MODULE_AT_TEST,
        )
    loaders = get_new_context()

    await add_comment(
        loaders=loaders,
        comment_data=comment_data,
        email=comment_data.email,
        event_id=comment_data.event_id,
        group_name=comment_data.group_name,
        parent_comment=comment_data.parent_id,
    )
    mocks_list = [mock[0] for mock in mocks_setup_list]
    assert all(mock_object.called is True for mock_object in mocks_list)


@pytest.mark.parametrize(
    ["group", "hacker_email", "attrs"],
    [
        [
            "unittesting",
            "unittesting@fluidattacks.com",
            {
                "context": "OTHER",
                "detail": "Something happened.",
                "event_date": datetime.fromisoformat(
                    "2019-12-09T05:00:00+00:00"
                ),
                "event_type": "AUTHORIZATION_SPECIAL_ATTACK",
                "root_id": "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            },
        ],
    ],
)
@patch(get_mocked_path("events_model.update_state"), new_callable=AsyncMock)
@patch(get_mocked_path("events_model.add"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.root.load"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.group.load"), new_callable=AsyncMock)
async def test_add_event(  # pylint: disable=too-many-arguments
    mock_group_loader: AsyncMock,
    mock_root_loader: AsyncMock,
    mock_db_model_event_add: AsyncMock,
    mock_db_model_event_update_state: AsyncMock,
    group: str,
    hacker_email: str,
    attrs: Any,
) -> None:
    mock_group_loader.return_value = get_mock_response(
        get_mocked_path("loaders.group.load"),
        json.dumps([group]),
    )
    mock_root_loader.return_value = get_mock_response(
        get_mocked_path("loaders.root.load"),
        json.dumps([group, attrs.get("root_id")]),
    )
    mock_db_model_event_add.return_value = get_mock_response(
        get_mocked_path("events_model.add"),
        json.dumps([group, hacker_email, attrs.get("root_id")]),
    )
    mock_db_model_event_update_state.return_value = get_mock_response(
        get_mocked_path("events_model.update_state"),
        json.dumps([group, hacker_email, attrs.get("root_id")]),
    )
    loaders = get_new_context()
    event_id = await add_event(
        loaders,
        hacker_email=hacker_email,
        group_name=group,
        **attrs,
    )
    assert isinstance(event_id, str)
    assert mock_group_loader.called is True
    assert mock_root_loader.called is True


@pytest.mark.parametrize(
    [
        "event_id",
        "group_name",
    ],
    [
        [
            "418900978",
            "oneshottest",
        ],
        [
            "538745942",
            "unittesting",
        ],
    ],
)
@patch(get_mocked_path("events_model.remove"), new_callable=AsyncMock)
@patch(
    get_mocked_path("event_comments_domain.remove_comments"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("remove_file_evidence"), new_callable=AsyncMock)
@patch(get_mocked_path("search_evidence"), new_callable=AsyncMock)
async def test_remove_event(  # pylint: disable=too-many-arguments
    mock_search_evidence: AsyncMock,
    mock_remove_file_evidence: AsyncMock,
    mock_event_comments_domain_remove_comments: AsyncMock,
    mock_events_model_remove: AsyncMock,
    event_id: str,
    group_name: str,
) -> None:
    mock_search_evidence.return_value = get_mock_response(
        get_mocked_path("search_evidence"),
        json.dumps([event_id, group_name]),
    )
    mock_remove_file_evidence.return_value = get_mock_response(
        get_mocked_path("remove_file_evidence"),
        json.dumps([event_id, group_name]),
    )
    mock_event_comments_domain_remove_comments.return_value = (
        get_mock_response(
            get_mocked_path("event_comments_domain.remove_comments"),
            json.dumps([event_id]),
        )
    )
    mock_events_model_remove.return_value = get_mock_response(
        get_mocked_path("event_comments_domain.remove_comments"),
        json.dumps([event_id]),
    )
    await remove_event(event_id, group_name)

    assert mock_search_evidence.called is True
    assert mock_remove_file_evidence.called is True
    assert mock_event_comments_domain_remove_comments.called is True
    assert mock_events_model_remove.called is True


@pytest.mark.parametrize(
    [
        "event_id",
        "hacker_email",
        "reason",
        "other",
        "group_name",
        "expected_result",
    ],
    [
        [
            "418900978",
            "unittest@fluidattacks.com",
            EventSolutionReason.OTHER,
            "Other info",
            "oneshottest",
            ({}, {}),
        ],
        [
            "538745942",
            "unittesting@fluidattacks.com",
            EventSolutionReason.PERMISSION_GRANTED,
            "Other info",
            "unittesting",
            ({}, {}),
        ],
    ],
)
@patch(get_mocked_path("events_model.update_state"), new_callable=AsyncMock)
@patch(
    get_mocked_path("loaders.event_vulnerabilities_loader.load"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("loaders.event.load"), new_callable=AsyncMock)
async def test_solve_event(  # pylint: disable=too-many-arguments
    mock_event_loader: AsyncMock,
    mock_event_vulnerabilities_loader_loader: AsyncMock,
    mock_db_model_event_update_state: AsyncMock,
    event_id: str,
    hacker_email: str,
    reason: EventSolutionReason,
    other: str,
    group_name: str,
    expected_result: tuple[dict[str, set[str]], dict[str, list[str]]],
) -> None:
    mock_event_loader.return_value = get_mock_response(
        get_mocked_path("loaders.event.load"),
        json.dumps([event_id]),
    )

    mock_event_vulnerabilities_loader_loader.return_value = get_mock_response(
        get_mocked_path("loaders.event_vulnerabilities_loader.load"),
        json.dumps([event_id]),
    )
    mock_db_model_event_update_state.return_value = get_mock_response(
        get_mocked_path("events_model.update_state"),
        json.dumps([event_id, hacker_email, reason, other, group_name]),
    )
    loaders: GraphQLResolveInfo = create_dummy_info(
        request=create_dummy_simple_session()
    )
    result = await solve_event(
        info=loaders,
        event_id=event_id,
        group_name=group_name,
        hacker_email=hacker_email,
        reason=reason,
        other=other,
    )
    assert result == expected_result
    assert mock_event_vulnerabilities_loader_loader.called is True
    assert mock_db_model_event_update_state.called is True

    with pytest.raises(InvalidEventSolvingReason):
        await solve_event(
            info=loaders,
            event_id=event_id,
            group_name=group_name,
            hacker_email=hacker_email,
            reason=EventSolutionReason.CLONED_SUCCESSFULLY,
            other=other,
        )

    # Modify mock response to raise exception
    mock_event_loader.return_value = get_mock_response(
        get_mocked_path("loaders.event.load"),
        json.dumps([event_id, "Already closed"]),
    )
    with pytest.raises(EventAlreadyClosed):
        assert await solve_event(
            info=loaders,
            event_id=event_id,
            group_name=group_name,
            hacker_email=hacker_email,
            reason=reason,
            other=other,
        )
    assert mock_event_loader.call_count == 3


@pytest.mark.parametrize(
    ["event_id", "evidence_type", "file_name", "update_date"],
    [
        [
            "418900978",
            EventEvidenceId.FILE_1,
            "test-file-records.csv",
            datetime.fromisoformat("2022-12-29 14:14:19.182591+00:00"),
        ],
        [
            "538745942",
            EventEvidenceId.FILE_1,
            "test-file-records.csv",
            datetime.fromisoformat("2022-12-29 14:14:19.182591+00:00"),
        ],
    ],
)
@patch(get_mocked_path("replace_different_format"), new_callable=AsyncMock)
@patch(get_mocked_path("events_model.update_evidence"), new_callable=AsyncMock)
@patch(get_mocked_path("save_evidence"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.event.load"), new_callable=AsyncMock)
async def test_update_evidence(  # pylint: disable=too-many-arguments
    mock_event_loader: AsyncMock,
    mock_save_evidence: AsyncMock,
    mock_events_model_update_evidence: AsyncMock,
    mock_replace_different_format: AsyncMock,
    event_id: str,
    evidence_type: EventEvidenceId,
    file_name: str,
    update_date: datetime,
) -> None:
    mock_event_loader.return_value = get_mock_response(
        get_mocked_path("loaders.event.load"),
        json.dumps([event_id]),
    )
    mock_save_evidence.return_value = get_mock_response(
        get_mocked_path("save_evidence"),
        json.dumps([event_id, file_name]),
    )
    mock_events_model_update_evidence.return_value = get_mock_response(
        get_mocked_path("events_model.update_evidence"),
        json.dumps(
            [event_id, file_name, update_date, evidence_type], default=str
        ),
    )
    mock_replace_different_format.return_value = get_mock_response(
        get_mocked_path("replace_different_format"),
        json.dumps([event_id, evidence_type]),
    )
    loaders: Dataloaders = get_new_context()
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/" + file_name)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, "text/csv")
        await update_evidence(
            loaders=loaders,
            event_id=event_id,
            evidence_id=evidence_type,
            file=uploaded_file,
            group_name="unittesting",
            update_date=update_date,
        )
    assert mock_event_loader.called is True
    assert mock_save_evidence.called is True
    assert mock_events_model_update_evidence.called is True
    assert mock_replace_different_format.called is True


@pytest.mark.parametrize(
    ["event_id", "evidence_type", "file_name", "update_date", "uses_mock"],
    [
        [
            "=malicious-code-here",
            EventEvidenceId.FILE_1,
            "test-file-records.csv",
            datetime.fromisoformat("2022-12-29 14:14:19.182591+00:00"),
            False,
        ],
        [
            "418900978",
            EventEvidenceId.FILE_1,
            "malicious;-code,-here.csv",
            datetime.fromisoformat("2022-12-29 14:14:19.182591+00:00"),
            True,
        ],
    ],
)
@patch(get_mocked_path("loaders.event.load"), new_callable=AsyncMock)
async def test_update_evidence_invalid(  # pylint: disable=too-many-arguments
    mock_event_loader: AsyncMock,
    event_id: str,
    evidence_type: EventEvidenceId,
    file_name: str,
    update_date: datetime,
    uses_mock: bool,
) -> None:
    if uses_mock:
        mock_event_loader.return_value = get_mock_response(
            get_mocked_path("loaders.event.load"),
            json.dumps([event_id]),
        )
    loaders: Dataloaders = get_new_context()
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/" + file_name)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, "text/csv")
        with pytest.raises(UnsanitizedInputFound):
            await update_evidence(
                loaders=loaders,
                event_id=event_id,
                evidence_id=evidence_type,
                file=uploaded_file,
                group_name="unittesting",
                update_date=update_date,
            )


@pytest.mark.parametrize(
    [
        "group_name",
        "evidence_type",
        "file_name",
        "organization_name",
        "allowed_mimes",
    ],
    [
        [
            "unittesting",
            EventEvidenceId.IMAGE_1,
            "test-file-records.csv",
            "okada",
            "images",
        ],
    ],
)
@patch(
    get_mocked_path("files_utils.assert_uploaded_file_mime"),
    new_callable=AsyncMock,
)
async def test_validate_evidence_invalid_file_type(
    # pylint: disable=too-many-arguments
    mock_assert_uploaded_file_mime: AsyncMock,
    group_name: str,
    evidence_type: EventEvidenceId,
    file_name: str,
    organization_name: str,
    allowed_mimes: bool,
) -> None:
    mock_assert_uploaded_file_mime.return_value = get_mock_response(
        get_mocked_path("files_utils.assert_uploaded_file_mime"),
        json.dumps([file_name, allowed_mimes]),
    )
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/" + file_name)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, "text/csv")
        with pytest.raises(InvalidFileType):
            await validate_evidence(
                group_name=group_name,
                organization_name=organization_name,
                evidence_id=evidence_type,
                file=uploaded_file,
            )


@pytest.mark.parametrize(
    [
        "group_name",
        "evidence_type",
        "file_name",
        "organization_name",
        "allowed_mimes",
    ],
    [
        [
            "unittesting",
            EventEvidenceId.IMAGE_1,
            "test-big-image.jpg",
            "okada",
            "images",
        ],
    ],
)
@patch(
    get_mocked_path("files_utils.assert_uploaded_file_mime"),
    new_callable=AsyncMock,
)
async def test_validate_evidence_invalid_file_size(
    # pylint: disable=too-many-arguments
    mock_assert_uploaded_file_mime: AsyncMock,
    group_name: str,
    evidence_type: EventEvidenceId,
    file_name: str,
    organization_name: str,
    allowed_mimes: bool,
) -> None:
    mock_assert_uploaded_file_mime.return_value = get_mock_response(
        get_mocked_path("files_utils.assert_uploaded_file_mime"),
        json.dumps([file_name, allowed_mimes]),
    )
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/" + file_name)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, "text/csv")
        with pytest.raises(InvalidFileSize):
            await validate_evidence(
                group_name=group_name,
                organization_name=organization_name,
                evidence_id=evidence_type,
                file=uploaded_file,
            )


@pytest.mark.parametrize(
    [
        "group_name",
        "evidence_type",
        "file_name",
        "organization_name",
        "allowed_mimes",
    ],
    [
        [
            "unittesting",
            EventEvidenceId.FILE_1,
            "test-file-records.csv",
            "okada",
            "files",
        ],
    ],
)
@patch(
    get_mocked_path("files_utils.assert_uploaded_file_mime"),
    new_callable=AsyncMock,
)
async def test_validate_evidence_invalid_file_name(
    # pylint: disable=too-many-arguments
    mock_assert_uploaded_file_mime: AsyncMock,
    group_name: str,
    evidence_type: EventEvidenceId,
    file_name: str,
    organization_name: str,
    allowed_mimes: bool,
) -> None:
    mock_assert_uploaded_file_mime.return_value = get_mock_response(
        get_mocked_path("files_utils.assert_uploaded_file_mime"),
        json.dumps([file_name, allowed_mimes]),
    )
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, "./mock/" + file_name)
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(file_name, test_file, "text/csv")
        with pytest.raises(InvalidFileName):
            await validate_evidence(
                group_name=group_name,
                organization_name=organization_name,
                evidence_id=evidence_type,
                file=uploaded_file,
            )
