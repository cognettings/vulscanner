from lib.root.f335.cloudformation import (
    cfn_s3_bucket_versioning_disabled,
)
from lib.root.f335.terraform import (
    tfm_s3_bucket_versioning_disabled,
)

__all__ = [
    "cfn_s3_bucket_versioning_disabled",
    "tfm_s3_bucket_versioning_disabled",
]
