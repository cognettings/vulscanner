from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.while_statement import (
    build_while_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block = match_ast_d(graph, args.n_id, "control_structure_body")

    if not block:
        raise MissingCaseHandling(
            f"Bad while statement handling in {args.n_id}"
        )

    conditional_node = adj_ast(graph, args.n_id)[2]

    return build_while_statement_node(args, block, conditional_node)
