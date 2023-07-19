from model import (
    core,
)
import os
import pytest
import subprocess
from utils.model import (
    is_cvssv3,
)


@pytest.mark.skims_test_group("unittesting")
def test_methods_utils() -> None:
    for _, member in core.MethodsEnum.__members__.items():
        assert is_cvssv3(member.value)


def _has_method_correct_information(method: core.MethodsEnum) -> bool:
    found = False
    method_info = method.value
    module_path = os.path.join(
        os.getcwd(), f"skims/skims/{method_info.module}"
    )
    file_options = [
        os.path.join(
            method_info.module, method_info.file_name
        ),  # lib/http/analyze_headers
        os.path.join(
            method_info.module,
            method_info.finding.name.lower(),
            method_info.file_name,
        ),  # lib/path/f001/java
        os.path.join(
            method_info.module,
            method_info.file_name,
            method_info.finding.name.lower(),
        ),  # lib/dast/aws/f001
    ]

    with subprocess.Popen(
        ["grep", "-lr", method.name, module_path], stdout=subprocess.PIPE
    ) as proc:
        stdout, _ = proc.communicate()
        if proc.returncode == 0:
            # For some methods, there may be several result paths
            results = stdout.decode().strip("\n").split("\n")
            found = any(
                result.split(".", maxsplit=1)[0].endswith(option)
                for option in file_options
                for result in results
            )

    return found


@pytest.mark.skims_test_group("unittesting")
def test_methods_model() -> None:
    for method in core.MethodsEnum:
        if "APK" in method.name:
            continue
        assert _has_method_correct_information(method)
