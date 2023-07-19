from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_TYPES = {
    "AuthenticationTypes.None",
    "AuthenticationTypes.Anonymous",
}


def cs_insec_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if f'{ma_attr["expression"]}.{ma_attr["member"]}' in DANGER_TYPES:
        args.evaluation[args.n_id] = True
        args.triggers.add("danger_auth")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
