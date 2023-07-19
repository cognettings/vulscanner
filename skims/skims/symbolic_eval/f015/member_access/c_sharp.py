from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_basic_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if f'{n_attrs["expression"]}.{n_attrs["member"]}' == "WebRequest.Create":
        args.evaluation[args.n_id] = True
        args.triggers.add("webreq")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
