from model.core import (
    MethodsEnum,
)
from symbolic_eval.f042.literal.c_sharp import (
    cs_insecure_cookies,
)
from symbolic_eval.f042.literal.common import (
    js_insecure_cookies,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_INSEC_COOKIES: cs_insecure_cookies,
    MethodsEnum.JS_INSEC_COOKIES: js_insecure_cookies,
    MethodsEnum.TS_INSEC_COOKIES: js_insecure_cookies,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
