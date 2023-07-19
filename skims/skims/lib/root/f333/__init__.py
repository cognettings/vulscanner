from lib.root.f333.cloudformation import (
    cfn_ec2_associate_public_ip_address,
    cfn_ec2_has_not_an_iam_instance_profile,
    cfn_ec2_has_terminate_shutdown_behavior,
)
from lib.root.f333.terraform import (
    tfm_ec2_associate_public_ip_address,
    tfm_ec2_has_not_an_iam_instance_profile,
    tfm_ec2_has_terminate_shutdown_behavior,
)

__all__ = [
    "cfn_ec2_associate_public_ip_address",
    "cfn_ec2_has_terminate_shutdown_behavior",
    "cfn_ec2_has_not_an_iam_instance_profile",
    "tfm_ec2_associate_public_ip_address",
    "tfm_ec2_has_not_an_iam_instance_profile",
    "tfm_ec2_has_terminate_shutdown_behavior",
]
