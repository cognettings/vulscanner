from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.catch_clause import (
    build_catch_clause_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    catch_node = args.ast_graph.nodes[args.n_id]
    block_node = catch_node["label_field_body"]
    param_id = catch_node.get("label_field_parameter")
    childs = (param_id,) if param_id else None
    return build_catch_clause_node(args, block_node, childs)
