from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

COOKIE = {"javax.servlet.http.Cookie", "Cookie"}


def java_insecure_cookie(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] in COOKIE:
        args.triggers.add("isCookieObject")
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
