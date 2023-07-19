from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.literal import (
    build_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    return build_literal_node(args, n_attrs["label_text"], "number")
