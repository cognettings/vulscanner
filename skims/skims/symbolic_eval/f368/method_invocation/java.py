from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_host_key_checking(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attr = args.graph.nodes[args.n_id]

    if n_attr["expression"] == "getSession":
        args.evaluation[args.n_id] = True
        args.triggers.add("sshSession")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
