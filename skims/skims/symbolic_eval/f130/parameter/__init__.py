from model.core import (
    MethodsEnum,
)
from symbolic_eval.f130.parameter.java import (
    java_insecure_cookie_response,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_SECURE_COOKIE: java_insecure_cookie_response,
    MethodsEnum.KOTLIN_SECURE_COOKIE: java_insecure_cookie_response,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
