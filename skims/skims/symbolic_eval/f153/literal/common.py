from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def allow_all_mime_types(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    node = args.graph.nodes[args.n_id]
    dang_values: set[str] = {"accept", "*/*"}
    if (node_val := node.get("value")) and (
        node_val.lower()[1:-1] in dang_values
    ):
        args.triggers.add(node_val.lower()[1:-1])
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
