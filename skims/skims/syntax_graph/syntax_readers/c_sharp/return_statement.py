from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.return_statment import (
    build_return_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "return", ";")

    if len(match) == 3 and match["return"] and match[";"]:
        return build_return_node(args, value_id=str(match["__0__"]))

    if len(match) == 2:
        return build_return_node(args, None)

    raise MissingCaseHandling(f"Bad return statement in {args.n_id}")
