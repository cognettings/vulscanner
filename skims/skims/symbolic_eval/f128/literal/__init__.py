from model.core import (
    MethodsEnum,
)
from symbolic_eval.f128.literal.java import (
    java_insecure_cookie,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_HTTP_ONLY_COOKIE: java_insecure_cookie,
    MethodsEnum.KOTLIN_HTTP_ONLY_COOKIE: java_insecure_cookie,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
