from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)

COOKIE = {"javax.servlet.http.Cookie", "Cookie"}


def kotlin_insecure_cookie_response(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    if args.graph.nodes[args.n_id]["variable_type"] in COOKIE or (
        (method := adj_ast(graph, args.n_id)[0])
        and graph.nodes[method]["expression"] in COOKIE
    ):
        args.triggers.add("isCookieObject")
        args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
