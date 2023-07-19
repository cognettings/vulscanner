from model.core import (
    FindingEnum,
)
from symbolic_eval.f015.import_node import (
    evaluate as evaluate_import_f015,
)
from symbolic_eval.f153.import_node import (
    evaluate as evaluate_import_f153,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F015: evaluate_import_f015,
    FindingEnum.F153: evaluate_import_f153,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
