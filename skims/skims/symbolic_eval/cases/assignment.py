from model.core import (
    FindingEnum,
)
from symbolic_eval.multifile.assignment import (
    evaluate_if_statement,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    op_attr = args.graph.nodes[args.n_id]
    # Danger should NOT propagate to the variable_id node because of FP risks
    if (
        args.graph_db
        and (if_nid := evaluate_if_statement(args))
        and (execution_node := args.graph.nodes[if_nid].get("execution_node"))
        and execution_node != args.n_id
    ):
        args.evaluation[args.n_id] = False
        return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)

    args.evaluation[args.n_id] = args.generic(
        args.fork_n_id(op_attr["value_id"])
    ).danger

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
