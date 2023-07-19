from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def danger_accept_header(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if str(args.graph.nodes[args.n_id].get("value"))[1:-1] == "*/*":
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
