from model.graph import (
    NId,
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
    name = node_to_str(args.ast_graph, name_id)
    block_id = class_node["label_field_body"]

    return build_class_node(args, name, block_id, None)
