from model.core import (
    FindingEnum,
)
from symbolic_eval.f001.member_access import (
    evaluate as evaluate_member_access_f001,
)
from symbolic_eval.f004.member_access import (
    evaluate as evaluate_member_access_f004,
)
from symbolic_eval.f008.member_access import (
    evaluate as evaluate_member_access_f008,
)
from symbolic_eval.f015.member_access import (
    evaluate as evaluate_member_access_f015,
)
from symbolic_eval.f016.member_access import (
    evaluate as evaluate_member_access_f016,
)
from symbolic_eval.f021.member_access import (
    evaluate as evaluate_member_access_f021,
)
from symbolic_eval.f034.member_access import (
    evaluate as evaluate_member_access_f034,
)
from symbolic_eval.f052.member_access import (
    evaluate as evaluate_member_access_f052,
)
from symbolic_eval.f060.member_access import (
    evaluate as evaluate_member_access_f060,
)
from symbolic_eval.f063.member_access import (
    evaluate as evaluate_member_access_f063,
)
from symbolic_eval.f085.member_access import (
    evaluate as evaluate_member_access_f085,
)
from symbolic_eval.f091.member_access import (
    evaluate as evaluate_member_access_f091,
)
from symbolic_eval.f096.member_access import (
    evaluate as evaluate_member_access_f096,
)
from symbolic_eval.f098.member_access import (
    evaluate as evaluate_member_access_f098,
)
from symbolic_eval.f107.member_access import (
    evaluate as evaluate_member_access_f107,
)
from symbolic_eval.f112.member_access import (
    evaluate as evaluate_member_access_f112,
)
from symbolic_eval.f127.member_access import (
    evaluate as evaluate_member_access_f127,
)
from symbolic_eval.f143.member_access import (
    evaluate as evaluate_member_access_f143,
)
from symbolic_eval.f211.member_access import (
    evaluate as evaluate_member_access_f211,
)
from symbolic_eval.f239.member_access import (
    evaluate as evaluate_member_access_f239,
)
from symbolic_eval.f280.member_access import (
    evaluate as evaluate_member_access_f280,
)
from symbolic_eval.f297.member_access import (
    evaluate as evaluate_member_access_f297,
)
from symbolic_eval.f313.member_access import (
    evaluate as evaluate_member_access_f313,
)
from symbolic_eval.f320.member_access import (
    evaluate as evaluate_member_access_f320,
)
from symbolic_eval.f413.member_access import (
    evaluate as evaluate_member_access_f413,
)
from symbolic_eval.f416.member_access import (
    evaluate as evaluate_member_access_f416,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F001: evaluate_member_access_f001,
    FindingEnum.F004: evaluate_member_access_f004,
    FindingEnum.F008: evaluate_member_access_f008,
    FindingEnum.F015: evaluate_member_access_f015,
    FindingEnum.F016: evaluate_member_access_f016,
    FindingEnum.F021: evaluate_member_access_f021,
    FindingEnum.F034: evaluate_member_access_f034,
    FindingEnum.F052: evaluate_member_access_f052,
    FindingEnum.F060: evaluate_member_access_f060,
    FindingEnum.F063: evaluate_member_access_f063,
    FindingEnum.F085: evaluate_member_access_f085,
    FindingEnum.F091: evaluate_member_access_f091,
    FindingEnum.F096: evaluate_member_access_f096,
    FindingEnum.F098: evaluate_member_access_f098,
    FindingEnum.F107: evaluate_member_access_f107,
    FindingEnum.F112: evaluate_member_access_f112,
    FindingEnum.F127: evaluate_member_access_f127,
    FindingEnum.F143: evaluate_member_access_f143,
    FindingEnum.F211: evaluate_member_access_f211,
    FindingEnum.F239: evaluate_member_access_f239,
    FindingEnum.F280: evaluate_member_access_f280,
    FindingEnum.F297: evaluate_member_access_f297,
    FindingEnum.F313: evaluate_member_access_f313,
    FindingEnum.F320: evaluate_member_access_f320,
    FindingEnum.F413: evaluate_member_access_f413,
    FindingEnum.F416: evaluate_member_access_f416,
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    children = g.adj_ast(args.graph, args.n_id)
    danger = [args.generic(args.fork_n_id(n_id)).danger for n_id in children]
    args.evaluation[args.n_id] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
