from model.core import (
    FindingEnum,
)
from symbolic_eval.f052.object import (
    evaluate as evaluate_object_f052,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F052: evaluate_object_f052,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    param_ids = adj_ast(args.graph, args.n_id)
    danger = [args.generic(args.fork_n_id(p_id)).danger for p_id in param_ids]
    args.evaluation[args.n_id] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
