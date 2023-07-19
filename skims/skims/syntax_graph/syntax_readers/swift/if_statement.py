from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    condition_id = (
        n_attrs.get("label_field_condition")
        or match_ast_d(graph, args.n_id, "simple_identifier")
        or match_ast_d(graph, args.n_id, "call_expression")
        or adj_ast(graph, args.n_id)[0]
    )

    statements = match_ast_group_d(graph, args.n_id, "statements")

    true_id = None
    false_id = None

    if len(statements) == 2:
        true_id = statements[0]
        false_id = statements[1]
    elif len(statements) == 1:
        true_id = statements[0]

    if false_statement := match_ast_d(graph, args.n_id, "if_statement"):
        false_id = false_statement

    return build_if_node(args, condition_id, true_id, false_id)
