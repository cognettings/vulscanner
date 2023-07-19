from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def java_weak_random(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if (
        n_attrs["expression"] == "random"
        and (obj_id := n_attrs.get("object_id"))
        and args.graph.nodes[obj_id].get("symbol") == "java.lang.Math"
    ):
        args.triggers.add("weakrandom")

    if n_attrs["expression"] == "setSecure":
        args.triggers.add("secure")
    if n_attrs["expression"] == "setHttpOnly":
        args.triggers.add("httponly")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
