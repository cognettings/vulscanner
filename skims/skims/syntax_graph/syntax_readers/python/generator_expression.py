from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    var_id = n_attrs["label_field_body"]
    val_id = match_ast_d(args.ast_graph, args.n_id, "for_in_clause")
    if not val_id:
        val_id = match_ast_d(args.ast_graph, args.n_id, "if_clause")
    return build_assignment_node(args, var_id, str(val_id), None)
