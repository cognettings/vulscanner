from model.core import (
    MethodsEnum,
)
from symbolic_eval.f016.object_creation.c_sharp import (
    cs_httpclient_revocation_lst,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_HTTPCLIENT_NO_REVOCATION_LIST: cs_httpclient_revocation_lst,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
