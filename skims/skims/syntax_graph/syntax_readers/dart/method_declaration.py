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
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    name_id = n_attrs["label_field_name"]
    name = node_to_str(graph, name_id)
    block_id = n_attrs.get("label_field_body")
    children_n_ids: dict[str, list[NId]] = {}
    parameters_id = n_attrs["label_field_parameters"]
    if "__0__" in match_ast(args.ast_graph, parameters_id, "(", ")"):
        children_n_ids.update({"parameters_id": [parameters_id]})

    return build_method_declaration_node(args, name, block_id, children_n_ids)
