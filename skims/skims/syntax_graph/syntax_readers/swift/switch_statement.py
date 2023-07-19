from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    value_id = args.ast_graph.nodes[args.n_id]["label_field_expr"]
    mock_body_id = str(int(args.n_id) + 1)
    child_ids = adj_ast(args.ast_graph, args.n_id)
    case_ids = (
        _id
        for _id in child_ids
        if args.ast_graph.nodes[_id]["label_type"] == "switch_entry"
    )
    args.syntax_graph.add_node(
        args.n_id,
        block_id=mock_body_id,
        value_id=value_id,
        label_type="SwitchStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(value_id)),
        label_ast="AST",
    )
    args.syntax_graph.add_node(
        mock_body_id,
        label_type="SwitchBody",
    )
    args.syntax_graph.add_edge(
        args.n_id,
        mock_body_id,
        label_ast="AST",
    )
    for c_id in case_ids:
        args.syntax_graph.add_edge(
            mock_body_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
