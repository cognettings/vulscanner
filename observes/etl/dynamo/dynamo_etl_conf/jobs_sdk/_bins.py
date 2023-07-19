from enum import (
    Enum,
)
from os import (
    environ,
)


class BinPaths(Enum):
    DYNAMO_CORE_PHASE_1 = environ["DYNAMO_PHASE_1"]
    DYNAMO_CORE_PHASE_3 = environ["DYNAMO_PHASE_3"]
    DETERMINE_SCHEMAS = environ["DYNAMO_DETERMINE_SCHEMA"]
    PREPARE_LOADING = environ["DYNAMO_PREPARE_LOADING"]
