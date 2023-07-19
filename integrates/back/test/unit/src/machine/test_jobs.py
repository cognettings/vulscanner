from machine.jobs import (
    get_finding_code_from_title,
)


def test_get_finding_code_from_title() -> None:
    spec_finding_code: str = "F416"
    finding_title: str = "416. XAML injection"
    finding_code = get_finding_code_from_title(finding_title)
    assert finding_code == spec_finding_code
