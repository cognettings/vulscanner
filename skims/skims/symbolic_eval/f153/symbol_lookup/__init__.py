from model.core import (
    MethodsEnum,
)
from symbolic_eval.f153.symbol_lookup.common import (
    allow_all_mime_types as http_req_allows_all_mime,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVASCRIPT_ACCEPTS_ANY_MIME_METHOD: http_req_allows_all_mime,
    MethodsEnum.TYPESCRIPT_ACCEPTS_ANY_MIME_METHOD: http_req_allows_all_mime,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
