from graphql import (
    ASTValidationRule,
    GraphQLError,
    OperationDefinitionNode,
)
from settings.api import (
    API_MAX_QUERY_BREADTH,
)


class QueryBreadthValidation(ASTValidationRule):
    """
    This validation prevents the execution of queries requesting an excessive
    amount of root resolvers to prevent abuse.
    """

    def enter_operation_definition(
        self, node: OperationDefinitionNode, *_args: None
    ) -> None:
        if len(node.selection_set.selections) > API_MAX_QUERY_BREADTH:
            self.report_error(
                GraphQLError("Exception - Max query breadth exceeded", node)
            )
