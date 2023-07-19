from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "getBytes",
    "getHeader",
    "getHeaderNames",
    "getHeaders",
    "getName",
    "getParameter",
    "getParameterMap",
    "getParameterNames",
    "getParameterValues",
    "getQueryString",
    "getValue",
}


def java_remote_command_execution(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    ma_attr = args.graph.nodes[args.n_id]

    if ma_attr["expression"] in DANGER_METHODS:
        args.triggers.add("userparams")
    if (
        ma_attr["expression"] == "getRuntime"
        and (obj_id := ma_attr.get("object_id"))
        and args.graph.nodes[obj_id].get("symbol") == "Runtime"
    ):
        args.evaluation[args.n_id] = True
        args.triggers.add("runtime")
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
