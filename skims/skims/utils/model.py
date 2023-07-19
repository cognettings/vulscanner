from cvss import (
    CVSS3,
    CVSS3Error,
)
from model.core import (
    MethodInfo,
)
from model.cvss3 import (
    find_score_data,
)


def is_cvssv3(method: MethodInfo) -> bool:
    try:
        CVSS3(
            method.cvss
            if method.cvss
            else find_score_data(method.get_finding()).score_to_vector_string()
        )
        return True
    except CVSS3Error:
        return False
