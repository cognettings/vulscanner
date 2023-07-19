from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.return_statment import (
    build_return_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    return_value = args.ast_graph.nodes[args.n_id].get("label_field_result")
    return build_return_node(args, return_value)
