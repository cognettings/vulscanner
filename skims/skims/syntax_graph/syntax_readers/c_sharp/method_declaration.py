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
    match_ast,
    match_ast_d,
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    declaration_n_id = match_ast_d(graph, args.n_id, "identifier")
    declaration_node = graph.nodes[declaration_n_id]
    declaration_line = declaration_node["label_l"]
    graph.nodes[args.n_id]["label_l"] = declaration_line
    name_id = n_attrs["label_field_name"]
    name = node_to_str(graph, name_id)
    block_id = n_attrs.get("label_field_body")

    parameters_id = n_attrs["label_field_parameters"]
    if "__0__" not in match_ast(graph, parameters_id, "(", ")"):
        parameters_list = []
    else:
        parameters_list = [parameters_id]

    attributes_id = match_ast_group_d(graph, args.n_id, "attribute_list")

    children_nid = {
        "attributes_id": attributes_id,
        "parameters_id": parameters_list,
    }
    return build_method_declaration_node(args, name, block_id, children_nid)
