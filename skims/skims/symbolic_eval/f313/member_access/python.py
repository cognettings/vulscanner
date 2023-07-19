from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)


def python_unsafe_cert(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]
    expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'
    if expr == "ssl.CERT_NONE":
        args.evaluation[args.n_id] = True
        args.triggers.add("cert_none")
    elif expr in {
        "ssl._create_unverified_context",
        "ssl.create_default_context",
    }:
        args.evaluation[args.n_id] = True
        args.triggers.add("sslcontext")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
