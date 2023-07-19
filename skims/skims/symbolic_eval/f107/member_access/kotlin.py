from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def kt_anonymous_ldap(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    member_access = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if member_access == "Context.SECURITY_AUTHENTICATION":
        args.evaluation[args.n_id] = True
        args.triggers.add("authContext")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
