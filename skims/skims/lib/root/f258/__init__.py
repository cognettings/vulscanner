from lib.root.f258.cloudformation import (
    cfn_elb2_has_not_deletion_protection,
)
from lib.root.f258.terraform import (
    tfm_elb2_has_not_deletion_protection,
)

__all__ = [
    "cfn_elb2_has_not_deletion_protection",
    "tfm_elb2_has_not_deletion_protection",
]
