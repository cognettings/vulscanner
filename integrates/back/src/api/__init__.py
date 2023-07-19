from .enums import (
    ENUMS,
)
from .resolvers import (
    TYPES,
)
from .scalars import (
    SCALARS,
)
from .types import (
    Operation,
)
from .unions import (
    UNIONS,
)
from .validations.characters import (
    validate_characters,
)
from .validations.directives import (
    validate_directives,
)
from .validations.query_breadth import (
    QueryBreadthValidation,
)
from .validations.query_depth import (
    QueryDepthValidation,
)
from .validations.variables_validation import (
    variables_check,
)
from ariadne import (
    load_schema_from_path,
    make_executable_schema,
)
from ariadne.asgi import (
    GraphQL,
)
from ariadne.asgi.handlers import (
    GraphQLHTTPHandler,
)
from ariadne.explorer import (
    ExplorerGraphiQL,
)
from ariadne.types import (
    QueryParser,
)
from custom_utils import (
    logs as logs_utils,
)
from dataloaders import (
    apply_context_attrs,
)
from dynamodb.types import (
    Item,
)
from graphql import (
    ASTValidationRule,
    DocumentNode,
)
import os
from settings.various import (
    DEBUG,
)
from starlette.requests import (
    Request,
)
import sys
from typing import (
    Any,
    Optional,
)


def _get_operation(data: Item) -> Operation:
    return Operation(
        name=data.get("operationName") or "External (unnamed)",
        query=data.get("query", "").replace("\n", "") or "-",
        variables=data.get("variables") or {},
    )


def _log_request(request: Request, operation: Operation) -> None:
    """
    Sends API operation metadata to cloud logging services for
    analytical purposes.
    """
    logs_utils.cloudwatch_log(
        request,
        f"API: {operation.name} with parameters {operation.variables}. "
        f"Complete query: {operation.query}",
    )


def hook_early_validations() -> None:
    """
    Hook into the execution process

    Warning: This is intended as a temporal workaround while some patches
    arrive upstream.
    """
    ariadne_graphql = sys.modules["ariadne.graphql"]
    original_parse = ariadne_graphql.parse_query

    def before_parse(
        context_value: Optional[Any],
        query_parser: Optional[QueryParser],
        data: Item,
    ) -> DocumentNode:
        validate_directives(data["query"])
        return original_parse(
            context_value=context_value, query_parser=query_parser, data=data
        )

    ariadne_graphql.parse_query = before_parse  # type: ignore


def get_validation_rules(
    context_value: Any | None,
    _document: DocumentNode,
    _data: Item,
) -> tuple[type[ASTValidationRule], ...]:
    return (  # type: ignore
        QueryBreadthValidation,
        QueryDepthValidation,
        validate_characters(context_value),
        variables_check(context_value),
    )


API_PATH = os.path.dirname(__file__)
SDL_CONTENT = "\n".join(
    [
        load_schema_from_path(os.path.join(API_PATH, module))
        for module in os.listdir(API_PATH)
        if os.path.isdir(os.path.join(API_PATH, module))
    ]
)
SCHEMA = make_executable_schema(
    SDL_CONTENT,
    *ENUMS,
    *SCALARS,
    *TYPES,
    *UNIONS,
    convert_names_case=True,
)


class IntegratesAPIHTTPHandler(GraphQLHTTPHandler):
    """
    Wrapper for the GraphQLHTTPHandler

    """

    async def get_context_for_request(
        self, request: Request, data: Item
    ) -> Request:
        data_dict: Item = await super().extract_data_from_request(request)
        operation = _get_operation(data_dict)
        context = apply_context_attrs(request)
        setattr(context, "operation", operation)

        return context

    async def extract_data_from_request(self, request: Request) -> Item:
        """Hook before the execution process begins"""
        data: Item = await super().extract_data_from_request(request)
        operation = _get_operation(data)

        _log_request(request, operation)

        return data


class IntegratesAPI(GraphQL):
    """
    Wrapper for the ariadne GraphQL initializer

    """

    def __init__(self) -> None:
        super().__init__(
            schema=SCHEMA,
            debug=DEBUG,
            http_handler=IntegratesAPIHTTPHandler(),
            validation_rules=get_validation_rules,
            explorer=ExplorerGraphiQL(
                title="API | Fluid Attacks", explorer_plugin=True
            ),
        )
        hook_early_validations()
