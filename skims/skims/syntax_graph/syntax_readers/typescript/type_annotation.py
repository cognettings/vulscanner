from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.unary_expression import (
    build_unary_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    match = match_ast(graph, args.n_id, ":")
    type_id = match.get("__0__") or adj_ast(graph, args.n_id)[-1]
    return build_unary_expression_node(args, "Typeof", type_id)
