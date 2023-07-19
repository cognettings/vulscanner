import json
from model import (
    core,
)
import os
import pytest
from zone import (
    t,
)


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_manifest_findings() -> None:
    path: str = "skims/manifests/findings.json"
    expected: str = (
        json.dumps(
            {
                finding.name: {
                    locale.name: dict(
                        title=t(finding.value.title, locale=locale),
                    )
                    for locale in core.LocalesEnum
                }
                for finding in core.FindingEnum
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    expected_path = os.path.join(os.environ["STATE"], path)
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w", encoding="utf-8") as handle_w:
        handle_w.write(expected)

    with open(path, encoding="utf-8") as handle_r:
        assert handle_r.read() == expected


@pytest.mark.skims_test_group("unittesting")
def test_model_core_model_manifest_queues() -> None:
    path: str = "skims/manifests/queues.json"
    expected: str = (
        json.dumps(
            {
                f"skims_{queue.name}": dict(
                    availability=queue.value.availability.value,
                    findings=sorted(
                        finding.name
                        for finding in core.FindingEnum
                        if finding.value.execution_queue == queue
                    ),
                )
                for queue in core.ExecutionQueue
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    expected_path = os.path.join(os.environ["STATE"], path)
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w", encoding="utf-8") as handle_w:
        handle_w.write(expected)

    with open(path, encoding="utf-8") as handle_r:
        assert handle_r.read() == expected
