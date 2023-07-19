from syntax_graph.syntax_readers.swift import (
    assignment as swift_assignment,
    binary_expression as swift_binary_expression,
    boolean_literal as swift_boolean_literal,
    call_expression as swift_call_expresion,
    class_body as swift_class_body,
    class_declaration as swift_class_declaration,
    comment as swift_comment,
    control_transfer as swift_control_transfer,
    do_statement as swift_do_statement,
    enum_entry as swift_enum_entry,
    expression_statement as swift_expression_statement,
    function_body as swift_function_body,
    function_declaration as swift_function_declaration,
    identifier as swift_identifier,
    if_nil_expression as swift_if_nil_expression,
    if_statement as swift_if_statement,
    import_statement as swift_import_statement,
    integer_literal as swift_integer_literal,
    navigation_expression as swift_navigation_expression,
    navigation_suffix as swift_navigation_suffix,
    nil as swift_nil,
    parameter as swift_parameter,
    prefix_expression as swift_prefix_expression,
    property_declaration as swift_property_declaration,
    source_file as swift_source_file,
    statements as swift_statements,
    string_literal as swift_string_literal,
    switch_entry as swift_switch_entry,
    switch_statement as swift_switch_statement,
    ternary_expression as swift_ternary_expression,
    try_expression as swift_try_expression,
    value_argument as swift_value_argument,
    value_arguments as swift_argument_list,
    while_statement as swift_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

SWIFT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "assignment",
        },
        syntax_reader=swift_assignment.reader,
    ),
    Dispatcher(
        applicable_types={
            "value_arguments",
        },
        syntax_reader=swift_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "additive_expression",
            "bitwise_operation",
            "comparison_expression",
            "conjunction_expression",
            "disjunction_expression",
            "equality_expression",
            "infix_expression",
            "multiplicative_expression",
        },
        syntax_reader=swift_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean_literal",
        },
        syntax_reader=swift_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=swift_call_expresion.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
            "enum_class_body",
            "protocol_body",
        },
        syntax_reader=swift_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
            "protocol_declaration",
        },
        syntax_reader=swift_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={"comment", "directive", "multiline_comment"},
        syntax_reader=swift_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "control_transfer_statement",
        },
        syntax_reader=swift_control_transfer.reader,
    ),
    Dispatcher(
        applicable_types={
            "enum_entry",
        },
        syntax_reader=swift_enum_entry.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=swift_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "directly_assignable_expression",
        },
        syntax_reader=swift_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "computed_property",
            "function_body",
        },
        syntax_reader=swift_function_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_declaration",
            "protocol_function_declaration",
        },
        syntax_reader=swift_function_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_literal",
            "as_expression",
            "constructor_expression",
            "identifier",
            "open_start_range_expression",
            "postfix_expression",
            "self_expression",
            "simple_identifier",
            "switch_pattern",
        },
        syntax_reader=swift_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "nil_coalescing_expression",
        },
        syntax_reader=swift_if_nil_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "guard_statement",
            "if_statement",
        },
        syntax_reader=swift_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_declaration",
        },
        syntax_reader=swift_import_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer_literal",
        },
        syntax_reader=swift_integer_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "navigation_expression",
        },
        syntax_reader=swift_navigation_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "navigation_suffix",
        },
        syntax_reader=swift_navigation_suffix.reader,
    ),
    Dispatcher(
        applicable_types={
            "nil",
        },
        syntax_reader=swift_nil.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter",
        },
        syntax_reader=swift_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "prefix_expression",
        },
        syntax_reader=swift_prefix_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_declaration",
            "protocol_property_declaration",
            "typealias_declaration",
        },
        syntax_reader=swift_property_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=swift_source_file.reader,
    ),
    Dispatcher(
        applicable_types={
            "statements",
        },
        syntax_reader=swift_statements.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_entry",
        },
        syntax_reader=swift_switch_entry.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_statement",
        },
        syntax_reader=swift_switch_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "dictionary_literal",
            "enum_type_parameters",
            "line_string_literal",
            "multi_line_string_literal",
            "tuple_expression",
            "user_type",
        },
        syntax_reader=swift_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "ternary_expression",
        },
        syntax_reader=swift_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_expression",
        },
        syntax_reader=swift_try_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "value_argument",
        },
        syntax_reader=swift_value_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=swift_while_statement.reader,
    ),
)
