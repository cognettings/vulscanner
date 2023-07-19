from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = (
        var_id
        for var_id in adj_ast(graph, args.n_id)
        if graph.nodes[var_id]["label_type"] not in {"{", "}", ","}
    )
    return build_expression_statement_node(args, c_ids)
