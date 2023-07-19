from lib.root.f070.cloudformation import (
    cfn_elb2_uses_insecure_security_policy,
)
from lib.root.f070.terraform import (
    tfm_elb2_uses_insecure_security_policy,
)

__all__ = [
    "cfn_elb2_uses_insecure_security_policy",
    "tfm_elb2_uses_insecure_security_policy",
]
