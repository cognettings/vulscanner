from model.core import (
    MethodsEnum,
)
from symbolic_eval.f052.variable_declaration.common import (
    insecure_sign_async,
)
from symbolic_eval.f052.variable_declaration.java import (
    java_insecure_hash,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_JWT_INSEC_SIGN_ALGO_ASYNC: insecure_sign_async,
    MethodsEnum.TS_JWT_INSEC_SIGN_ALGO_ASYNC: insecure_sign_async,
    MethodsEnum.JAVA_INSECURE_HASH: java_insecure_hash,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
