from lib.root.f134.c_sharp import (
    c_sharp_insecure_cors,
    c_sharp_insecure_cors_origin_attribute,
    c_sharp_insecure_cors_origin_method,
)
from lib.root.f134.cloudformation import (
    cfn_cors_true,
    cfn_wildcard_in_allowed_origins,
)
from lib.root.f134.java import (
    java_insecure_cors_origin,
    java_insecure_cors_origin_modifier,
)
from lib.root.f134.terraform import (
    tfm_wildcard_in_allowed_origins,
)

__all__ = [
    "c_sharp_insecure_cors",
    "c_sharp_insecure_cors_origin_attribute",
    "c_sharp_insecure_cors_origin_method",
    "cfn_cors_true",
    "cfn_wildcard_in_allowed_origins",
    "java_insecure_cors_origin",
    "java_insecure_cors_origin_modifier",
    "tfm_wildcard_in_allowed_origins",
]
