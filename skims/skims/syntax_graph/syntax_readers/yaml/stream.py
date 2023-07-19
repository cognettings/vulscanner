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
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    if (body_id := match_ast_d(args.ast_graph, args.n_id, "document")) and (
        block_id := match_ast_d(args.ast_graph, body_id, "block_node")
    ):
        filtered_ids = (
            _id
            for _id in adj_ast(args.ast_graph, block_id)
            if args.ast_graph.nodes[_id]["label_type"] != "---"
        )
        return build_file_node(args, iter(filtered_ids))

    return args.n_id
