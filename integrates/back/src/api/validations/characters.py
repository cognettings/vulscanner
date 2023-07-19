from api.types import (
    Operation,
)
from custom_utils.validations import (
    check_alnum,
)
from graphql import (
    ASTValidationRule,
    GraphQLError,
    ValidationContext,
)
from settings.api import (
    API_MAX_CHARACTERS,
)
from typing import (
    Any,
)


def validate_characters(context_value: Any) -> ASTValidationRule:
    """
    This validation prevents the execution of queries containing
    an excessive amount of characters and ensures that the query
    operation name is alphanumeric, thus effectively preventing abuse
    and maintaining security measures.
    """
    operation: Operation = context_value.operation

    class CharactersThresholdValidation(ASTValidationRule):
        def __init__(self, context: ValidationContext) -> None:
            super().__init__(context)

            if len(operation.query) > API_MAX_CHARACTERS:
                self.report_error(
                    GraphQLError("Exception - Max characters exceeded")
                )

            if (
                operation.name is not None
                and operation.name != "External (unnamed)"
                and not check_alnum(operation.name)
            ):
                self.report_error(
                    GraphQLError("Exception - Invalid operation name")
                )

    return CharactersThresholdValidation  # type: ignore
