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
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    block_node = args.ast_graph.nodes[args.n_id]["label_field_body"]
    childs = match_ast(
        args.ast_graph,
        args.n_id,
        "catch_declaration",
        "catch_filter_clause",
    )
    children = filter(
        None,
        [childs.get("catch_declaration"), childs.get("catch_filter_clause")],
    )

    return build_catch_clause_node(args, block_node, children)
