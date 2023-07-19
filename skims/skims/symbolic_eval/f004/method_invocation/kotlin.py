from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kotlin_remote_command_execution(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if ma_attr["expression"] == "Runtime.getRuntime":
        args.evaluation[args.n_id] = True
        args.triggers.add("getRuntime")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
