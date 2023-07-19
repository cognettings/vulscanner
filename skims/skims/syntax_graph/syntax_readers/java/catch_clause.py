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
    block = args.ast_graph.nodes[args.n_id]["label_field_body"]
    param_id = match_ast_d(args.ast_graph, args.n_id, "catch_formal_parameter")
    childs = (param_id,) if param_id else None
    return build_catch_clause_node(args, block, childs)
