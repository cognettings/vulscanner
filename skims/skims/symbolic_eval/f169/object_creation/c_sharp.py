from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_plain_text_cred(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["name"] == "CryptLib":
        args.evaluation[args.n_id] = True
        args.triggers.add("cryptlib")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
