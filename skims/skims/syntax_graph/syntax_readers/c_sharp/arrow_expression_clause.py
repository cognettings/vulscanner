from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    _, block_node = adj_ast(args.ast_graph, args.n_id)
    return build_method_declaration_node(args, "ArrowMethod", block_node, {})
