from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.catch_clause import (
    build_catch_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block = match_ast_d(graph, args.n_id, "statements")
    param_id = match_ast_d(graph, args.n_id, "simple_identifier")
    childs = (param_id,) if param_id else None
    return build_catch_clause_node(args, block, childs)
