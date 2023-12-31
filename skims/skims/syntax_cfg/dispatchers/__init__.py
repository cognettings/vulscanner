from syntax_cfg.dispatchers import (
    connect_to_block,
    connect_to_declarations,
    connect_to_next,
    end_node,
    if_node,
    method_invocation_node,
    multi_path,
    step_by_step,
    variable_declaration_node,
)
from syntax_cfg.types import (
    Dispatcher,
    Dispatchers,
)

DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "Class",
            "DoStatement",
            "ElseClause",
            "ForEachStatement",
            "ForStatement",
            "MethodDeclaration",
            "Namespace",
            "SwitchStatement",
            "UsingStatement",
            "WhileStatement",
        },
        cfg_builder=connect_to_block.build,
    ),
    Dispatcher(
        applicable_types={
            "ArgumentList",
            "BinaryOperation",
            "DeclarationBlock",
            "File",
            "TryStatement",
            "SwitchBody",
            "SwitchSection",
            "ClassBody",
        },
        cfg_builder=multi_path.build,
    ),
    Dispatcher(
        applicable_types={
            "ExecutionBlock",
            "ParameterList",
        },
        cfg_builder=step_by_step.build,
    ),
    Dispatcher(
        applicable_types={
            "If",
            "TernaryOperation",
        },
        cfg_builder=if_node.build,
    ),
    Dispatcher(
        applicable_types={
            "MethodInvocation",
        },
        cfg_builder=method_invocation_node.build,
    ),
    Dispatcher(
        applicable_types={
            "Annotation",
            "Argument",
            "ArrayInitializer",
            "Assignment",
            "Attribute",
            "AwaitExpression",
            "Break",
            "CatchClause",
            "CatchDeclaration",
            "Comment",
            "Continue",
            "Debugger",
            "ElementAccess",
            "ExpressionStatement",
            "FinallyClause",
            "JsxElement",
            "Literal",
            "MemberAccess",
            "MissingNode",
            "Modifiers",
            "NamedArgument",
            "NewExpression",
            "Object",
            "ObjectCreation",
            "Pair",
            "Parameter",
            "ParenthesizedExpression",
            "ReservedWord",
            "RestPattern",
            "Selector",
            "SpreadElement",
            "SymbolLookup",
            "TernaryOperation",
            "This",
            "ThrowStatement",
            "UnaryExpression",
            "Yield",
        },
        cfg_builder=connect_to_next.build,
    ),
    Dispatcher(
        applicable_types={
            "VariableDeclaration",
        },
        cfg_builder=variable_declaration_node.build,
    ),
    Dispatcher(
        applicable_types={
            "Return",
            "Export",
        },
        cfg_builder=connect_to_declarations.build,
    ),
    Dispatcher(
        applicable_types={
            "Import",
        },
        cfg_builder=end_node.build,
    ),
)
