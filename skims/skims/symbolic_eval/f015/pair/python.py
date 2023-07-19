from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_danger_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]
    key = n_attrs["key_id"]
    value = n_attrs["value_id"]
    if (
        str(args.graph.nodes[key].get("value"))[1:-1].lower()
        == "authorization"
        and args.generic(args.fork(n_id=value)).danger
    ):
        args.triggers.add("danger_auth")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
