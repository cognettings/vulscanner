from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_remote_command_execution(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if "SeparateClassRequest" in ma_attr["name"]:
        args.triggers.add("userparams")
    if ma_attr["name"] == "ProcessBuilder":
        args.evaluation[args.n_id] = True
        args.triggers.add("pbuilder")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
