from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_basic_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    val_str = str(args.graph.nodes[args.n_id]["value"][1:-1])
    if val_str.startswith("Basic "):
        args.evaluation[args.n_id] = True
        args.triggers.add("basicauth")
    elif val_str == "Authorization":
        args.evaluation[args.n_id] = True
        args.triggers.add("authconfig")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
