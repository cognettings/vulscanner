from model.core import (
    MethodsEnum,
)
from symbolic_eval.f052.pair.common import (
    insecure_key_pair,
    insecure_mode,
    insecure_sign,
    insecure_sign_async,
)
from symbolic_eval.f052.pair.python import (
    check_pair_key,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JS_INSECURE_ENCRYPT: insecure_mode,
    MethodsEnum.TS_INSECURE_ENCRYPT: insecure_mode,
    MethodsEnum.JS_INSECURE_EC_KEYPAIR: insecure_key_pair,
    MethodsEnum.TS_INSECURE_EC_KEYPAIR: insecure_key_pair,
    MethodsEnum.JS_INSECURE_RSA_KEYPAIR: insecure_key_pair,
    MethodsEnum.TS_INSECURE_RSA_KEYPAIR: insecure_key_pair,
    MethodsEnum.JS_JWT_INSEC_SIGN_ALGORITHM: insecure_sign,
    MethodsEnum.TS_JWT_INSEC_SIGN_ALGORITHM: insecure_sign,
    MethodsEnum.JS_JWT_INSEC_SIGN_ALGO_ASYNC: insecure_sign_async,
    MethodsEnum.TS_JWT_INSEC_SIGN_ALGO_ASYNC: insecure_sign_async,
    MethodsEnum.PYTHON_INSEC_SIGN_ALGORITHM: check_pair_key,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
