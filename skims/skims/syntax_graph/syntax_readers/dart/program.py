from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.file import (
    build_file_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_ids = adj_ast(args.ast_graph, args.n_id)
    ignored_types = {
        ";",
        "inferred_type",
        "function_body",
        "const_builtin",
        "late",
        "type_identifier",
        "final_builtin",
    }
    filtered_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_types
    ]
    return build_file_node(args, iter(filtered_ids))
