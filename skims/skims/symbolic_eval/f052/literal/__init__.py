from model.core import (
    MethodsEnum,
)
from symbolic_eval.f052.literal.c_sharp import (
    cs_disabled_strong_crypto,
    cs_insecure_keys,
    cs_insecure_sign_algo,
    cs_rsa_secure_mode,
)
from symbolic_eval.f052.literal.common import (
    insecure_create_cipher,
    insecure_sign_mechanism,
)
from symbolic_eval.f052.literal.java import (
    java_evaluate_cipher,
    java_insecure_cipher_jmqi,
    java_insecure_cipher_ssl,
    java_insecure_hash,
    java_insecure_key_ec,
    java_insecure_key_rsa,
    java_uses_unsafe_alg,
)
from symbolic_eval.f052.literal.javascript import (
    insecure_ecdh_key,
    insecure_hash,
    insecure_key_pair,
)
from symbolic_eval.f052.literal.kotlin import (
    kt_insecure_cipher,
    kt_insecure_cipher_ssl,
    kt_insecure_hash,
    kt_insecure_key,
    kt_insecure_key_ec,
    kt_insecure_key_gen,
    kt_insecure_parm_espec,
)
from symbolic_eval.f052.literal.python import (
    py_check_insec_alg,
)
from symbolic_eval.f052.literal.swift import (
    swift_insecure_crypto,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.CS_DISABLED_STRONG_CRYPTO: cs_disabled_strong_crypto,
    MethodsEnum.CS_INSECURE_KEYS: cs_insecure_keys,
    MethodsEnum.CS_INSEC_SIGN_ALGORITHM: cs_insecure_sign_algo,
    MethodsEnum.CS_RSA_SECURE_MODE: cs_rsa_secure_mode,
    MethodsEnum.JAVA_INSECURE_CIPHER: java_evaluate_cipher,
    MethodsEnum.JAVA_INSECURE_CIPHER_SSL: java_insecure_cipher_ssl,
    MethodsEnum.JAVA_INSECURE_CIPHER_JMQI: java_insecure_cipher_jmqi,
    MethodsEnum.JAVA_INSECURE_HASH: java_insecure_hash,
    MethodsEnum.JAVA_INSECURE_KEY_EC: java_insecure_key_ec,
    MethodsEnum.JAVA_INSECURE_KEY_RSA: java_insecure_key_rsa,
    MethodsEnum.JAVA_INSECURE_KEY_SECRET: java_evaluate_cipher,
    MethodsEnum.JAVA_INSEC_SIGN_ALGORITHM: java_uses_unsafe_alg,
    MethodsEnum.JS_INSECURE_CREATE_CIPHER: insecure_create_cipher,
    MethodsEnum.JS_INSECURE_ECDH_KEY: insecure_ecdh_key,
    MethodsEnum.TS_INSECURE_ECDH_KEY: insecure_ecdh_key,
    MethodsEnum.JS_INSECURE_EC_KEYPAIR: insecure_key_pair,
    MethodsEnum.JS_INSECURE_HASH: insecure_hash,
    MethodsEnum.KT_INSECURE_CIPHER: kt_insecure_cipher,
    MethodsEnum.KT_INSECURE_CIPHER_SSL: kt_insecure_cipher_ssl,
    MethodsEnum.KT_INSECURE_HASH: kt_insecure_hash,
    MethodsEnum.KT_INSECURE_KEY_PAIR_GEN: kt_insecure_key,
    MethodsEnum.KT_INSECURE_KEY: kt_insecure_key,
    MethodsEnum.KT_INSECURE_KEY_EC: kt_insecure_key_ec,
    MethodsEnum.KT_INSECURE_KEY_GEN: kt_insecure_key_gen,
    MethodsEnum.KT_INSECURE_PARAMETER_SPEC: kt_insecure_parm_espec,
    MethodsEnum.KT_INSECURE_ENCRIPTION_KEY: kt_insecure_parm_espec,
    MethodsEnum.TS_INSECURE_CREATE_CIPHER: insecure_create_cipher,
    MethodsEnum.TS_INSECURE_EC_KEYPAIR: insecure_key_pair,
    MethodsEnum.TS_INSECURE_HASH: insecure_hash,
    MethodsEnum.JS_INSECURE_RSA_KEYPAIR: insecure_key_pair,
    MethodsEnum.TS_INSECURE_RSA_KEYPAIR: insecure_key_pair,
    MethodsEnum.JS_INSEC_MSG_AUTH_MECHANISM: insecure_sign_mechanism,
    MethodsEnum.TS_INSEC_MSG_AUTH_MECHANISM: insecure_sign_mechanism,
    MethodsEnum.SWIFT_INSECURE_CRYPTOR: swift_insecure_crypto,
    MethodsEnum.PYTHON_INSEC_SIGN_ALGORITHM: py_check_insec_alg,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
