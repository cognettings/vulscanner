from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

hashing_method = {"createHash", "crypto.createHash"}


def js_check_hashes_salt(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]["expression"]
    if ma_attr in {"createHash", "crypto.createHash"}:
        args.evaluation[args.n_id] = True
        args.triggers.add("createHash")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
