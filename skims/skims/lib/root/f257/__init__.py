from lib.root.f257.cloudformation import (
    cfn_ec2_has_not_termination_protection,
)
from lib.root.f257.terraform import (
    tfm_ec2_has_not_termination_protection,
)

__all__ = [
    "cfn_ec2_has_not_termination_protection",
    "tfm_ec2_has_not_termination_protection",
]
