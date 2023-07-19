from dataloaders import (
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
    ToeInputEdge,
    ToeInputRequest,
    ToeInputsConnection,
    ToeInputState,
)
from dynamodb.types import (
    PageInfo,
)
import pytest

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group() -> None:
    group_name = "unittesting"
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load(
        GroupToeInputsRequest(group_name=group_name)
    )
    assert group_toe_inputs == ToeInputsConnection(
        edges=(
            ToeInputEdge(
                node=ToeInput(
                    component="https://test.com/test2/test.aspx",
                    entry_point="-",
                    group_name="unittesting",
                    state=ToeInputState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        attacked_by="test2@test.com",
                        be_present=True,
                        be_present_until=None,
                        has_vulnerabilities=False,
                        first_attack_at=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-01-11T05:00:00+00:00"
                        ),
                        seen_first_time_by="test2@test.com",
                        unreliable_root_id=(
                            "4039d098-ffc5-4984-8ed3-eb17bca98e19"
                        ),
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJ"
                    "TlBVVFMjUk9PVCM0MDM5ZDA5OC1mZmM1LTQ5ODQtOGVkMy1l"
                    "YjE3YmNhOThlMTkjQ09NUE9ORU5UI2h0dHBzOi8vdGVzdC5j"
                    "b20vdGVzdDIvdGVzdC5hc3B4I0VOVFJZUE9JTlQjLSJ9"
                ),
            ),
            ToeInputEdge(
                node=ToeInput(
                    component="https://test.com/test2/test.aspx",
                    entry_point="idTest (en-us)",
                    group_name="unittesting",
                    state=ToeInputState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        attacked_by="test2@test.com",
                        be_present=True,
                        be_present_until=None,
                        first_attack_at=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        has_vulnerabilities=False,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-01-11T05:00:00+00:00"
                        ),
                        seen_first_time_by="test2@test.com",
                        unreliable_root_id=(
                            "4039d098-ffc5-4984-8ed3-eb17bca98e19"
                        ),
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJ"
                    "TlBVVFMjUk9PVCM0MDM5ZDA5OC1mZmM1LTQ5ODQtOGVkMy1l"
                    "YjE3YmNhOThlMTkjQ09NUE9ORU5UI2h0dHBzOi8vdGVzdC5j"
                    "b20vdGVzdDIvdGVzdC5hc3B4I0VOVFJZUE9JTlQjaWRUZXN0"
                    "IChlbi11cykifQ=="
                ),
            ),
            ToeInputEdge(
                node=ToeInput(
                    component="https://test.com/api/Test",
                    entry_point="idTest",
                    group_name="unittesting",
                    state=ToeInputState(
                        attacked_at=datetime.fromisoformat(
                            "2020-01-02T05:00:00+00:00"
                        ),
                        attacked_by="test@test.com",
                        be_present=True,
                        be_present_until=None,
                        first_attack_at=datetime.fromisoformat(
                            "2020-01-02T05:00:00+00:00"
                        ),
                        has_vulnerabilities=False,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2000-01-01T05:00:00+00:00"
                        ),
                        seen_first_time_by="",
                        unreliable_root_id="",
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJTlBVVF"
                    "MjUk9PVCNDT01QT05FTlQjaHR0cHM6Ly90ZXN0LmNvbS9hcGkvVGVz"
                    "dCNFTlRSWVBPSU5UI2lkVGVzdCJ9"
                ),
            ),
            ToeInputEdge(
                node=ToeInput(
                    component="https://test.com/test/test.aspx",
                    entry_point="btnTest",
                    group_name="unittesting",
                    state=ToeInputState(
                        attacked_at=datetime.fromisoformat(
                            "2021-02-02T05:00:00+00:00"
                        ),
                        attacked_by="test@test.com",
                        be_present=False,
                        be_present_until=datetime.fromisoformat(
                            "2021-03-20T15:41:04+00:00"
                        ),
                        first_attack_at=datetime.fromisoformat(
                            "2021-01-02T05:00:00+00:00"
                        ),
                        has_vulnerabilities=False,
                        modified_by="test2@test.com",
                        modified_date=datetime.fromisoformat(
                            "2021-02-11T05:00:00+00:00"
                        ),
                        seen_at=datetime.fromisoformat(
                            "2020-03-14T05:00:00+00:00"
                        ),
                        seen_first_time_by="test@test.com",
                        unreliable_root_id="",
                    ),
                ),
                cursor=(
                    "eyJwayI6ICJHUk9VUCN1bml0dGVzdGluZyIsICJzayI6ICJJTlBV"
                    "VFMjUk9PVCNDT01QT05FTlQjaHR0cHM6Ly90ZXN0LmNvbS90ZXN0"
                    "L3Rlc3QuYXNweCNFTlRSWVBPSU5UI2J0blRlc3QifQ=="
                ),
            ),
        ),
        page_info=PageInfo(has_next_page=False, end_cursor="bnVsbA=="),
    )

    historic_toe_inputs = await loaders.toe_input_historic.load(
        ToeInputRequest(
            component="https://test.com/test2/test.aspx",
            entry_point="-",
            group_name=group_name,
            root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
        )
    )

    assert historic_toe_inputs == [
        ToeInput(
            component="https://test.com/test2/test.aspx",
            entry_point="-",
            group_name=group_name,
            state=ToeInputState(
                attacked_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                attacked_by="test2@test.com",
                be_present=True,
                be_present_until=None,
                first_attack_at=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                has_vulnerabilities=False,
                modified_by="test2@test.com",
                modified_date=datetime.fromisoformat(
                    "2021-02-11T05:00:00+00:00"
                ),
                seen_at=datetime.fromisoformat("2020-01-11T05:00:00+00:00"),
                seen_first_time_by="test2@test.com",
                unreliable_root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            ),
        ),
    ]
