from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

DANGER_METHODS = {
    "getBytes",
    "getHeader",
    "headerNames",
    "getHeaders",
    "name",
    "getParameter",
    "parameterMap",
    "parameterNames",
    "getParameterValues",
    "queryString",
    "getValue",
}


def kt_vuln_regex(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    expression = ma_attr["expression"].split(".")
    if expression[-1] in DANGER_METHODS:
        args.triggers.add("UserParams")

    if expression[-1] == "escape":
        exp_id = ma_attr["expression_id"]
        method = args.graph.nodes[exp_id]["expression"]
        if method == "Regex":
            args.triggers.add("SafeRegex")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
