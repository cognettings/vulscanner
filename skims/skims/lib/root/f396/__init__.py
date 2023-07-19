from lib.root.f396.cloudformation import (
    cfn_kms_key_is_key_rotation_absent_or_disabled,
)
from lib.root.f396.terraform import (
    tfm_kms_key_is_key_rotation_absent_or_disabled,
)

__all__ = [
    "cfn_kms_key_is_key_rotation_absent_or_disabled",
    "tfm_kms_key_is_key_rotation_absent_or_disabled",
]
