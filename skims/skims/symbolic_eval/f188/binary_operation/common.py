from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def has_origin_check(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    left_id = args.graph.nodes[args.n_id]["left_id"]
    if (
        expression := args.graph.nodes[left_id].get("expression")
    ) and expression == "origin":
        args.triggers.add("origin_comparison")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
