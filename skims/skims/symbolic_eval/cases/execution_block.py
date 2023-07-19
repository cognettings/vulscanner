from model.core import (
    FindingEnum,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    if args.n_id in args.path:
        deps_ids = tuple(args.path[: args.path.index(args.n_id)])
    else:
        deps_ids = adj_ast(args.graph, args.n_id)

    danger = [args.generic(args.fork_n_id(_id)).danger for _id in deps_ids]
    args.evaluation[args.n_id] = any(danger)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
