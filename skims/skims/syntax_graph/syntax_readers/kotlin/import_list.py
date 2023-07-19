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
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)

    for child in c_ids[:-1]:
        args.generic(args.fork_n_id(child))

    return args.generic(args.fork_n_id(c_ids[-1]))
