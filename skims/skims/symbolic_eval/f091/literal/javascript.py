from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def javascript_insecure_logging(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    sanitize = {
        '"[\\n\\r\\t]"',
        "/\\n|\\r/g",
    }
    if args.graph.nodes[args.n_id]["value"] in sanitize:
        args.triggers.add("characters")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
