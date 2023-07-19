from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.object import (
    build_object_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    get_ast_childs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    match_identifier = graph.nodes[args.n_id]["label_field_name"]
    property_name = graph.nodes[match_identifier].get("label_text")

    accessors = get_ast_childs(
        graph, args.n_id, "accessor_declaration", depth=2
    )

    return build_object_node(args, iter(accessors), property_name)
