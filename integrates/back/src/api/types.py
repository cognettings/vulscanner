from custom_exceptions import (
    CustomBaseException,
)
from dynamodb.exceptions import (
    DynamoDbBaseException,
)
from dynamodb.types import (
    Item,
)
from typing import (
    NamedTuple,
)

APP_EXCEPTIONS = (CustomBaseException, DynamoDbBaseException)


class Operation(NamedTuple):
    name: str
    query: str
    variables: Item
