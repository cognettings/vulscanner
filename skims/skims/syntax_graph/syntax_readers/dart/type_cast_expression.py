from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.binary_operation import (
    build_binary_operation_node,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    invalid_childs = {";", "type_cast", "(", ")"}

    if (
        len(c_ids) == 2
        and (type_cast := match_ast_d(graph, args.n_id, "type_cast"))
        and (
            typed_assignment := match_ast(graph, type_cast, "as_operator").get(
                "__0__"
            )
        )
    ):
        return build_binary_operation_node(
            args, "as", c_ids[0], typed_assignment
        )

    return build_expression_statement_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] not in invalid_childs
        ),
    )
