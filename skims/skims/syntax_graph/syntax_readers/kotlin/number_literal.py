from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.literal import (
    build_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    value = n_attrs.get("label_text") or node_to_str(graph, args.n_id)
    return build_literal_node(args, value, "number")
