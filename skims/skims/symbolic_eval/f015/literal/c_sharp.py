from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_basic_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value"][1:-1] == "Basic ":
        args.evaluation[args.n_id] = True
        args.triggers.add("basicauth")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
