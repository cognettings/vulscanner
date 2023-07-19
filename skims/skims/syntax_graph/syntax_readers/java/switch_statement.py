from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.switch_statement import (
    build_switch_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    body_id = args.ast_graph.nodes[args.n_id]["label_field_body"]
    condition_id = args.ast_graph.nodes[args.n_id]["label_field_condition"]
    return build_switch_statement_node(args, body_id, condition_id)
