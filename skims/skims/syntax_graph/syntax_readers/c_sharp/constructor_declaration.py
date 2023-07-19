from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    method = args.ast_graph.nodes[args.n_id]
    name_id = method["label_field_name"]
    name = node_to_str(args.ast_graph, name_id)
    block_id = method["label_field_body"]
    children = {
        "parameters_id": [
            method["label_field_parameters"],
        ],
    }

    return build_method_declaration_node(args, name, block_id, children)
