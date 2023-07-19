from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.spread_element import (
    build_spread_element_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "...")
    identifier_id = match.get("__0__")
    if not identifier_id:
        raise MissingCaseHandling(f"Bad spread element in {args.n_id}")

    return build_spread_element_node(args, identifier_id)
