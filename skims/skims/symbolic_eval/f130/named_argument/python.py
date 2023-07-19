from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

COOKIE_SET = {"secure"}


def python_insecure_cookie(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["argument_name"] in COOKIE_SET:
        value = args.graph.nodes[args.n_id]["value_id"]
        if args.graph.nodes[value]["value"] == "False":
            args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
