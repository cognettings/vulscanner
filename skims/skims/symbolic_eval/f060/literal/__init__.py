from model.core import (
    MethodsEnum,
)
from symbolic_eval.f060.literal.c_sharp import (
    cs_insecure_certificate,
)
from symbolic_eval.f060.literal.python import (
    python_ssl_hostname,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_INSECURE_CERTIFICATE_VALIDATION: cs_insecure_certificate,
    MethodsEnum.PYTHON_UNSAFE_SSL_HOSTNAME: python_ssl_hostname,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
