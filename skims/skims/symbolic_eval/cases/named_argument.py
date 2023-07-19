from model.core import (
    FindingEnum,
)
from symbolic_eval.f052.named_argument import (
    evaluate as evaluate_method_f052,
)
from symbolic_eval.f128.named_argument import (
    evaluate as evaluate_method_f128,
)
from symbolic_eval.f130.named_argument import (
    evaluate as evaluate_method_f130,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F052: evaluate_method_f052,
    FindingEnum.F128: evaluate_method_f128,
    FindingEnum.F130: evaluate_method_f130,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False

    value_id = args.graph.nodes[args.n_id].get("value_id")
    args.evaluation[args.n_id] = args.generic(args.fork_n_id(value_id)).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
