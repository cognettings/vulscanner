from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    var_name = node_to_str(args.ast_graph, n_attrs["label_field_name"])

    type_id = n_attrs["label_field_value"]
    if args.ast_graph.nodes[type_id]["label_type"] == "generic_type":
        var_type = node_to_str(args.ast_graph, type_id)
    else:
        var_type = args.ast_graph.nodes[type_id]["label_type"]

    return build_variable_declaration_node(args, var_name, var_type, None)
