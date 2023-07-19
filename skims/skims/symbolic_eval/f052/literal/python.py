from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def py_check_insec_alg(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    value = n_attrs.get("value")

    if value[1:-1] == "HS256":
        args.triggers.add("HS256")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
