from lib.root.f408.cloudformation import (
    cfn_api_gateway_access_logging_disabled,
)
from lib.root.f408.terraform import (
    tfm_api_gateway_access_logging_disabled,
)

__all__ = [
    "tfm_api_gateway_access_logging_disabled",
    "cfn_api_gateway_access_logging_disabled",
]
