from model.core import (
    MethodsEnum,
)
from symbolic_eval.f112.method_invocation.common import (
    unsafe_sql_injection,
)
from symbolic_eval.f112.method_invocation.java import (
    java_sql_injection,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_SQL_INJECTION: java_sql_injection,
    MethodsEnum.JS_SQL_API_INJECTION: unsafe_sql_injection,
    MethodsEnum.TS_SQL_API_INJECTION: unsafe_sql_injection,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
