from graphql import (
    ASTValidationRule,
    FieldNode,
    GraphQLError,
    ValidationContext,
)
from settings.api import (
    API_MAX_QUERY_DEPTH,
)


class QueryDepthValidation(ASTValidationRule):
    """
    This validation prevents the execution of queries requesting an excessive
    amount of nested cyclic resolvers to prevent abuse.

    Inspired by graphql-ruby's implementation
    """

    def __init__(self, context: ValidationContext) -> None:
        super().__init__(context)
        self.current_depth = 0

    def enter_field(self, *_args: None) -> None:
        self.current_depth += 1

    def leave_field(self, node: FieldNode, *_args: None) -> None:
        if self.current_depth > API_MAX_QUERY_DEPTH:
            self.report_error(
                GraphQLError("Exception - Max query depth exceeded", node)
            )

        self.current_depth -= 1
