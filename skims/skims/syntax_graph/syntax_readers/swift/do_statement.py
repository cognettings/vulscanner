from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.try_statement import (
    build_try_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    block_id = match_ast_d(graph, args.n_id, "statements")
    catch_id = match_ast_d(graph, args.n_id, "catch_block")
    catch_statements = match_ast_d(graph, str(catch_id), "statements")
    return build_try_statement_node(
        args, str(block_id), [str(catch_statements)], None, None
    )
