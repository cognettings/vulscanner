from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_host_key_checking(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "JSch":
        args.triggers.add("jshObject")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
