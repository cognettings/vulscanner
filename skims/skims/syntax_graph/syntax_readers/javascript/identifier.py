from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.symbol_lookup import (
    build_symbol_lookup_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    symbol = args.ast_graph.nodes[args.n_id]["label_text"]
    return build_symbol_lookup_node(args, symbol)
