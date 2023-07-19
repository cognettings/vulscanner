from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def py_algorithm_argument(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    node = args.graph.nodes[args.n_id]
    if (arg_name := node.get("argument_name")) and (arg_name == "algorithm"):
        args.triggers.add("algorithm")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
