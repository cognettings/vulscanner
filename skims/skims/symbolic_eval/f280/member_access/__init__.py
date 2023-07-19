from model.core import (
    MethodsEnum,
)
from symbolic_eval.f280.member_access.common import (
    is_user_input,
)
from symbolic_eval.f280.member_access.python import (
    xml_parser,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_NON_SECURE_CONSTRUCTION_OF_COOKIES: is_user_input,
    MethodsEnum.PYTHON_SESSION_FIXATION: xml_parser,
    MethodsEnum.TS_NON_SECURE_CONSTRUCTION_OF_COOKIES: is_user_input,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
