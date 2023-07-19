from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_ssl_hostname(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if expr in {
        "ssl._create_unverified_context",
        "ssl.create_default_context",
    }:
        args.evaluation[args.n_id] = True
        args.triggers.add("sslcontext")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
