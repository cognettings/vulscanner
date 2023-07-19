from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    label_text = node_to_str(args.ast_graph, args.n_id)
    if text_nid := n_attrs.get("label_field_text"):
        label_text = args.ast_graph.nodes[text_nid]["label_text"]
    return build_string_literal_node(args, label_text)
