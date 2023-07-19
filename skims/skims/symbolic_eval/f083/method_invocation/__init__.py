from model.core import (
    MethodsEnum,
)
from symbolic_eval.f083.method_invocation.java import (
    xml_parser,
)
from symbolic_eval.f083.method_invocation.kotlin import (
    kt_xml_parser,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

METHOD_EVALUATORS: dict[MethodsEnum, Evaluator] = {
    MethodsEnum.JAVA_XML_PARSER: xml_parser,
    MethodsEnum.KT_XML_PARSER: kt_xml_parser,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if language_evaluator := METHOD_EVALUATORS.get(args.method):
        return language_evaluator(args)
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
