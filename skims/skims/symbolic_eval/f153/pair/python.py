from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def danger_accept_header(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    if (
        str(args.graph.nodes[key].get("value"))[1:-1].lower() == "accept"
        and args.generic(args.fork(n_id=value)).danger
    ):
        args.triggers.add("danger_accept")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
