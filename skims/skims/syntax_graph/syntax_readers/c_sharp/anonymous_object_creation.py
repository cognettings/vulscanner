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
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    ignore_types = {"new", "{", "(", "}", ")", ",", "name_equals"}
    filtered_ids = (
        _id
        for _id in c_ids
        if graph.nodes[_id]["label_type"] not in ignore_types
    )

    return build_object_node(args, filtered_ids, "AnonymousObject")
