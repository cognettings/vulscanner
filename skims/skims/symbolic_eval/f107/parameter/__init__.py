from model.core import (
    MethodsEnum,
)
from symbolic_eval.f107.parameter.c_sharp import (
    cs_ldap_injection,
)
from symbolic_eval.f107.parameter.java import (
    java_ldap_injection,
)
from symbolic_eval.f107.parameter.kotlin import (
    kt_anonymous_ldap,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_LDAP_INJECTION: cs_ldap_injection,
    MethodsEnum.JAVA_LDAP_INJECTION: java_ldap_injection,
    MethodsEnum.KT_ANONYMOUS_LDAP: kt_anonymous_ldap,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
