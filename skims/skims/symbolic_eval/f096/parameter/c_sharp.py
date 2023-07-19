from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def cs_xml_serial(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if args.graph.nodes[args.n_id]["variable_type"] == "HttpRequest":
        args.evaluation[args.n_id] = True
        args.triggers.add("HttpRequest")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
