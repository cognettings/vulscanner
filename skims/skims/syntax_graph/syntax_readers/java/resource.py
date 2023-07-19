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
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    value_id = n_attrs.get("label_field_value")
    var_name = node_to_str(graph, n_attrs["label_field_name"])
    type_id = n_attrs.get("label_field_type")
    var_type = node_to_str(graph, type_id) if type_id else None

    return build_variable_declaration_node(args, var_name, var_type, value_id)
