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
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    var_ids = match_ast_group_d(args.ast_graph, args.n_id, "identifier")
    return build_expression_statement_node(args, iter(var_ids))
