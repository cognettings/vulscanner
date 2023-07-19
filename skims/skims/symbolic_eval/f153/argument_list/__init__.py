from model.core import (
    MethodsEnum,
)
from symbolic_eval.f153.argument_list.c_sharp import (
    allow_all_mime_types as c_sharp_allows_all_mime_types,
)
from symbolic_eval.f153.argument_list.java import (
    allow_all_mime_types as java_allows_all_mime_types,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_HTTP_REQ_ACCEPTS_ANY_MIMETYPE: java_allows_all_mime_types,
    MethodsEnum.C_SHARP_ACCEPTS_ANY_MIMETYPE: c_sharp_allows_all_mime_types,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
