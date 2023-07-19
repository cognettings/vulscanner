from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kotlin_remote_command_execution(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpServletRequest":
        args.evaluation[args.n_id] = True
        args.triggers.add("UserConnection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
