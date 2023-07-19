from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    invalid_types = {"[", "]", "{", "}", ",", ";"}

    valid_seqs = [
        child
        for child in adj_ast(graph, args.n_id)
        if graph.nodes[child]["label_type"] not in invalid_types
    ]

    usable_ids = []
    for _id in valid_seqs:
        childs = adj_ast(graph, _id)
        if len(childs) < 2:
            continue
        current_id = childs[1]

        if graph.nodes[current_id]["label_type"] != "block_node":
            usable_ids.append(current_id)
        elif (current_id_childs := adj_ast(graph, current_id)) and len(
            current_id_childs
        ) > 0:
            if graph.nodes[current_id_childs[0]]["label_type"] == "tag":
                usable_ids.append(current_id_childs[-1])
            else:
                usable_ids.append(current_id_childs[0])

    return build_array_node(args, usable_ids)
