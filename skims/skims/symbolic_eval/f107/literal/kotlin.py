from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kt_anonymous_ldap(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    if (
        n_attrs["value_type"] == "string"
        and n_attrs["value"].strip("'\"") == "none"
    ):
        args.evaluation[args.n_id] = True
        args.triggers.add("anonymous")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
