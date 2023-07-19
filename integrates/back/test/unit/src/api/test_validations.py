from api import (
    get_validation_rules,
    hook_early_validations,
    SCHEMA,
)
from api.types import (
    Operation,
)
from graphql import (
    get_introspection_query,
    GraphQLError,
    parse,
    validate,
)
import pytest
from settings.api import (
    API_MAX_CHARACTERS,
    API_MAX_DIRECTIVES,
)
import sys
from typing import (
    NamedTuple,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


class ContextValue(NamedTuple):
    operation: Operation


_context_value = ContextValue(
    operation=Operation(name="", query="", variables={})
)


def test_should_allow_introspection() -> None:
    query = get_introspection_query()
    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(_context_value, parse(query), {}),
    )
    assert not errors


def test_should_validate_depth() -> None:
    query = """
        query MaliciousQuery {
            __schema {
                queryType {
                    name
                    kind
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                    ofType {
                                        kind
                                        name
                                        ofType {
                                            kind
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    """
    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(_context_value, parse(query), {}),
    )
    assert errors
    assert errors[0].message == "Exception - Max query depth exceeded"


def test_should_validate_breadth() -> None:
    query = """
        query MaliciousQuery {
            alias1: __schema {
                queryType {
                    name
                    kind
                }
            }
            alias2: __schema {
                queryType {
                    name
                    kind
                }
            }
            alias3: __schema {
                queryType {
                    name
                    kind
                }
            }
            alias4: __schema {
                queryType {
                    name
                    kind
                }
            }
        }
    """
    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(_context_value, parse(query), {}),
    )
    assert errors
    assert errors[0].message == "Exception - Max query breadth exceeded"


def test_should_validate_variables() -> None:
    query = """
        mutation ExtraVariables (
            $test: String!,
            $name: String!,
        ) {
            mutationName(
                test: $test
                name: $name
            ) {
                success
            }
        }
    """

    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(
            ContextValue(
                operation=Operation(
                    name="",
                    query="",
                    variables={
                        "test": "value",
                        "name": "value",
                        "extra_variable": "value",
                    },
                )
            ),
            parse(query),
            {},
        ),
    )
    assert errors
    assert errors[0].message == "Exception - Extra variables in operation"


def test_should_validate_directives() -> None:
    query = f"""
        query MaliciousQuery {{
            __typename
            {"@aa " * (API_MAX_DIRECTIVES + 1)}
        }}
    """

    hook_early_validations()
    with pytest.raises(GraphQLError):
        sys.modules["ariadne.graphql"].parse_query(
            context_value=None, query_parser=None, data={"query": query}
        )


def test_should_validate_characters() -> None:
    query = f"""
        query MaliciousQuery {{
            {"a" * (API_MAX_CHARACTERS + 1)}: __typename
        }}
    """

    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(
            ContextValue(
                operation=Operation(name="", query=query, variables={})
            ),
            parse(query),
            {},
        ),
    )
    assert errors
    assert errors[0].message == "Exception - Max characters exceeded"


def test_should_validate_alphanumeric() -> None:
    query = """
        query MaliciousQuery {
            alias1: __schema {
                queryType {
                    name
                    kind
                }
            }
        }
    """

    errors = validate(
        SCHEMA,
        parse(query),
        get_validation_rules(
            ContextValue(
                operation=Operation(name="<script>", query=query, variables={})
            ),
            parse(query),
            {},
        ),
    )
    assert errors
    assert errors[0].message == "Exception - Invalid operation name"
