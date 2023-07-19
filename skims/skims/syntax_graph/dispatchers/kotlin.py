from syntax_graph.syntax_readers.kotlin import (
    argument_list as kotlin_argument_list,
    assignment_expression as kotlin_assignment_expression,
    binary_expression as kotlin_binary_expression,
    boolean_literal as kotlin_boolean_literal,
    catch_clause as kotlin_catch_clause,
    class_body as kotlin_class_body,
    class_declaration as kotlin_class_declaration,
    comment as kotlin_comment,
    companion_object as kotlin_companion_object,
    expression_statement as kotlin_expression_statement,
    finally_clause as kotlin_finally_clause,
    for_statement as kotlin_for_statement,
    identifier as kotlin_identifier,
    if_statement as kotlin_if_statement,
    import_declaration as kotlin_import_declaration,
    import_list as kotlin_import_list,
    infix_expression as kotlin_infix_expression,
    jump_statement as kotlin_jump_statement,
    member_access_expression as kotlin_member_access_expression,
    method_declaration as kotlin_method_declaration,
    method_invocation as kotlin_method_invocation,
    number_literal as kotlin_number_literal,
    object as kotlin_object,
    parameter as kotlin_parameter,
    parenthesized_expression as kotlin_parenthesized_expression,
    program as kotlin_program,
    reserved_word as kotlin_reserved_word,
    statement_block as kotlin_declaration_block,
    statements as kotlin_statements,
    string_literal as kotlin_string_literal,
    try_statement as kotlin_try_statement,
    variable_declaration as kotlin_variable_declaration,
    when_entry as kotlin_when_entry,
    when_expression as kotlin_when_expression,
    while_statement as kotlin_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

KOTLIN_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "value_arguments",
        },
        syntax_reader=kotlin_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "elvis_expression",
        },
        syntax_reader=kotlin_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "additive_expression",
            "assignment",
            "check_expression",
            "comparison_expression",
            "conjunction_expression",
            "disjunction_expression",
            "equality_expression",
            "multiplicative_expression",
            "range_expression",
        },
        syntax_reader=kotlin_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean_literal",
        },
        syntax_reader=kotlin_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_block",
        },
        syntax_reader=kotlin_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
        },
        syntax_reader=kotlin_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=kotlin_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "line_comment",
            "multiline_comment",
        },
        syntax_reader=kotlin_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "companion_object",
        },
        syntax_reader=kotlin_companion_object.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_body",
            "control_structure_body",
        },
        syntax_reader=kotlin_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "directly_assignable_expression",
        },
        syntax_reader=kotlin_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "finally_block",
        },
        syntax_reader=kotlin_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_statement",
        },
        syntax_reader=kotlin_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "postfix_expression",
            "simple_identifier",
            "type_identifier",
        },
        syntax_reader=kotlin_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_expression",
        },
        syntax_reader=kotlin_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_header",
            "package_header",
        },
        syntax_reader=kotlin_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_list",
        },
        syntax_reader=kotlin_import_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "jump_expression",
        },
        syntax_reader=kotlin_jump_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "navigation_expression",
        },
        syntax_reader=kotlin_member_access_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "anonymous_initializer",
            "function_declaration",
        },
        syntax_reader=kotlin_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=kotlin_method_invocation.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer_literal",
            "real_literal",
        },
        syntax_reader=kotlin_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object_declaration",
            "object_literal",
        },
        syntax_reader=kotlin_object.reader,
    ),
    Dispatcher(
        applicable_types={
            "infix_expression",
        },
        syntax_reader=kotlin_infix_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter",
            "value_argument",
        },
        syntax_reader=kotlin_parameter.reader,
    ),
    Dispatcher(
        applicable_types={"parenthesized_expression"},
        syntax_reader=kotlin_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=kotlin_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "null",
            "super_expression",
            "this_expression",
        },
        syntax_reader=kotlin_reserved_word.reader,
    ),
    Dispatcher(
        applicable_types={
            "long_literal",
            "navigation_suffix",
            "string_literal",
        },
        syntax_reader=kotlin_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "statements",
        },
        syntax_reader=kotlin_statements.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_expression",
        },
        syntax_reader=kotlin_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_declaration",
        },
        syntax_reader=kotlin_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "when_entry",
        },
        syntax_reader=kotlin_when_entry.reader,
    ),
    Dispatcher(
        applicable_types={
            "when_expression",
        },
        syntax_reader=kotlin_when_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=kotlin_while_statement.reader,
    ),
)
