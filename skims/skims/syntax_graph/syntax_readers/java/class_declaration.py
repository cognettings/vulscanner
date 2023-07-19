from model.graph import (
    NId,
)
from syntax_graph.metadata.java import (
    add_class_to_metadata,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    class_node = args.ast_graph.nodes[args.n_id]
    name_id = class_node["label_field_name"]
    block_id = class_node["label_field_body"]
    name = node_to_str(args.ast_graph, name_id)

    if args.syntax_graph.nodes.get("0"):
        add_class_to_metadata(args, name)

    return build_class_node(args, name, block_id, None)
