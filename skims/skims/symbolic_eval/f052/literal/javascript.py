from symbolic_eval.common import (
    INSECURE_HASHES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    crypto,
)


def insecure_ecdh_key(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] in {"string"}:
        value = args.graph.nodes[args.n_id]["value"][1:-1]
        args.evaluation[args.n_id] = crypto.insecure_elliptic_curve(value)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] == "string":
        member_str = args.graph.nodes[args.n_id]["value"]
        if any(hash in member_str.lower() for hash in INSECURE_HASHES):
            args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)


def insecure_key_pair(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.graph.nodes[args.n_id]["value_type"] in {"string"}:
        value = args.graph.nodes[args.n_id]["value"][1:-1]
        if value == "rsa":
            args.triggers.add("rsa")
        elif value == "ec":
            args.triggers.add("ec")
        elif crypto.insecure_elliptic_curve(value):
            args.evaluation[args.n_id] = True

    if args.graph.nodes[args.n_id]["value_type"] in {"number"}:
        value = args.graph.nodes[args.n_id]["value"]
        try:
            key_int = int(value)
            if key_int < 2048:
                args.evaluation[args.n_id] = True
        except ValueError:
            args.evaluation[args.n_id] = False

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
