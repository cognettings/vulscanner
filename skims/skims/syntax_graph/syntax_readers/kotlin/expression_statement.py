from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    expr_ids = adj_ast(args.ast_graph, args.n_id)
    return build_expression_statement_node(args, iter(expr_ids))
