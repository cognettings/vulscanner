from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def check_pair_key(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    nodes = args.graph.nodes
    key_n_id = nodes[args.n_id].get("key_id")
    key_val = nodes[key_n_id].get("value")

    if key_val[1:-1] == "alg":
        args.triggers.add("alg")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
