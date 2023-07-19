from model.core import (
    MethodsEnum,
)
from symbolic_eval.f134.literal.c_sharp import (
    cs_insecure_cors_origin,
)
from symbolic_eval.f134.literal.java import (
    java_insecure_cors_origin,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_INSECURE_CORS_ORIGIN: cs_insecure_cors_origin,
    MethodsEnum.JAVA_INSECURE_CORS_ORIGIN: java_insecure_cors_origin,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
