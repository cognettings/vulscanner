from model.core import (
    MethodsEnum,
)
from symbolic_eval.f015.literal.c_sharp import (
    cs_basic_auth,
)
from symbolic_eval.f015.literal.java import (
    java_basic_auth,
)
from symbolic_eval.f015.literal.python import (
    python_danger_auth,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_INSECURE_AUTHENTICATION: cs_basic_auth,
    MethodsEnum.JAVA_BASIC_AUTHENTICATION: java_basic_auth,
    MethodsEnum.PYTHON_INSECURE_AUTHENTICATION: python_danger_auth,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
