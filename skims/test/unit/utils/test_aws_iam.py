import pytest
from utils.aws_iam import (
    is_action_permissive,
    is_resource_permissive,
    match_pattern,
)


@pytest.mark.skims_test_group("unittesting")
def test_match_pattern() -> None:
    base_pattern: str = "iam:PassRole"
    assert match_pattern(base_pattern, base_pattern)
    assert match_pattern("iam:PassR*", base_pattern)
    assert match_pattern("iam:Pass*", base_pattern)
    assert match_pattern("iam:P*", base_pattern)
    assert match_pattern("iam:*PassRole", base_pattern)
    assert match_pattern("iam:*PassR*", base_pattern)
    assert match_pattern("iam:*Pass*", base_pattern)
    assert match_pattern("iam:*P*", base_pattern)
    assert match_pattern("iam:*", base_pattern)
    assert match_pattern("iam*", base_pattern)
    assert match_pattern("*:PassRole", base_pattern)
    assert match_pattern("*:*Pass*", base_pattern)
    assert match_pattern("*", base_pattern)
    assert match_pattern(".*", ".iam:PassRole")
    assert not match_pattern("a*", base_pattern)
    assert not match_pattern("iam", base_pattern)
    assert not match_pattern("iam:PassRol", base_pattern)
    # Ensure symbolic chars in a regex context are properly escaped
    assert not match_pattern(".", "x")
    assert not match_pattern("iam:PassRol.", base_pattern)
    assert not match_pattern("iam:Pa.sRol.", base_pattern)
    assert not match_pattern("............", base_pattern)
    assert not match_pattern(".*", base_pattern)


@pytest.mark.skims_test_group("unittesting")
def test_is_action_permissive() -> None:
    assert is_action_permissive("*")
    assert is_action_permissive("s3:*")
    assert is_action_permissive("s3*")
    assert is_action_permissive("s3*:*")
    assert is_action_permissive("s3******:*")

    assert not is_action_permissive("s3:")
    assert not is_action_permissive("s3:xx")
    assert not is_action_permissive("s3:xx*")
    assert not is_action_permissive("s3:x*x*")
    assert not is_action_permissive("s3*:")
    assert not is_action_permissive("s3***:")

    assert not is_action_permissive(None)
    assert not is_action_permissive({})
    assert not is_action_permissive([])


@pytest.mark.skims_test_group("unittesting")
def test_is_resource_permissive() -> None:
    assert is_resource_permissive("*")
    assert not is_resource_permissive("arn:aws:iam::*:role/cloud-lambda")
