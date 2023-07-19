from model.core import (
    FindingEnum,
)
from model.graph import (
    Graph,
    NId,
)
from sast import (
    SUPPORTED_MULTIFILE,
)
from symbolic_eval.context.data_structure import (
    search_data_element,
)
from symbolic_eval.context.method import (
    solve_invocation,
)
from symbolic_eval.f004.method_invocation import (
    evaluate as evaluate_method_f004,
)
from symbolic_eval.f008.method_invocation import (
    evaluate as evaluate_method_f008,
)
from symbolic_eval.f015.method_invocation import (
    evaluate as evaluate_method_f015,
)
from symbolic_eval.f021.method_invocation import (
    evaluate as evaluate_method_f021,
)
from symbolic_eval.f034.method_invocation import (
    evaluate as evaluate_method_f034,
)
from symbolic_eval.f052.method_invocation import (
    evaluate as evaluate_method_f052,
)
from symbolic_eval.f059.method_invocation import (
    evaluate as evaluate_method_f059,
)
from symbolic_eval.f063.method_invocation import (
    evaluate as evaluate_method_f063,
)
from symbolic_eval.f083.method_invocation import (
    evaluate as evaluate_method_f083,
)
from symbolic_eval.f089.method_invocation import (
    evaluate as evaluate_method_f089,
)
from symbolic_eval.f091.method_invocation import (
    evaluate as evaluate_method_f091,
)
from symbolic_eval.f107.method_invocation import (
    evaluate as evaluate_method_f107,
)
from symbolic_eval.f112.method_invocation import (
    evaluate as evaluate_method_f112,
)
from symbolic_eval.f153.method_invocation import (
    evaluate as evaluate_method_f153,
)
from symbolic_eval.f211.method_invocation import (
    evaluate as evaluate_method_f211,
)
from symbolic_eval.f280.method_invocation import (
    evaluate as evaluate_method_f280,
)
from symbolic_eval.f338.method_invocation import (
    evaluate as evaluate_method_f338,
)
from symbolic_eval.f344.method_invocation import (
    evaluate as evaluate_method_f344,
)
from symbolic_eval.f368.method_invocation import (
    evaluate as evaluate_method_f368,
)
from symbolic_eval.multifile.method_invocation import (
    evaluate_method_invocation,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from symbolic_eval.utils import (
    get_inv_forward_paths,
    iter_backward_paths,
)
from utils import (
    graph as g,
)
from utils.fs import (
    decide_language,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F004: evaluate_method_f004,
    FindingEnum.F008: evaluate_method_f008,
    FindingEnum.F015: evaluate_method_f015,
    FindingEnum.F034: evaluate_method_f034,
    FindingEnum.F021: evaluate_method_f021,
    FindingEnum.F052: evaluate_method_f052,
    FindingEnum.F059: evaluate_method_f059,
    FindingEnum.F063: evaluate_method_f063,
    FindingEnum.F083: evaluate_method_f083,
    FindingEnum.F089: evaluate_method_f089,
    FindingEnum.F091: evaluate_method_f091,
    FindingEnum.F107: evaluate_method_f107,
    FindingEnum.F112: evaluate_method_f112,
    FindingEnum.F153: evaluate_method_f153,
    FindingEnum.F211: evaluate_method_f211,
    FindingEnum.F280: evaluate_method_f280,
    FindingEnum.F338: evaluate_method_f338,
    FindingEnum.F344: evaluate_method_f344,
    FindingEnum.F368: evaluate_method_f368,
}

MODIFYING_METHODS: set[str] = {"add", "push", "put", "get"}


def assign_method_declaration_parameters_eval(
    graph: Graph, evaluation: dict[NId, bool], md_id: NId, mi_id: NId
) -> dict[NId, bool]:
    if (
        (al_id := graph.nodes[mi_id].get("arguments_id"))
        and (pl_id := graph.nodes[md_id].get("arguments_id"))
        and (p_ids := g.adj_ast(graph, pl_id))
        and (a_ids := g.adj_ast(graph, al_id))
        and len(p_ids) != len(a_ids)
    ):
        invocation_eval = {}
        for p_id, a_id in zip(p_ids, a_ids):
            invocation_eval[p_id] = evaluation[a_id]
        return invocation_eval
    return {}


def evaluate_method_expression(
    args: SymbolicEvalArgs,
    expr_id: NId,
) -> bool:
    if args.graph.nodes[expr_id].get("symbol") in MODIFYING_METHODS:
        return False

    if md_id := solve_invocation(args.graph, args.path, expr_id):
        if eb_id := args.graph.nodes[md_id].get("block_id"):
            invoc_eval = assign_method_declaration_parameters_eval(
                args.graph, args.evaluation, md_id, mi_id=args.n_id
            )
            d_expression = any(
                args.generic(
                    args.fork(
                        n_id=eb_id, path=fwd + bck, evaluation=invoc_eval
                    )
                ).danger
                for fwd in get_inv_forward_paths(args.graph, eb_id)
                for _, *bck in iter_backward_paths(args.graph, eb_id)
            )
        else:
            d_expression = args.generic(args.fork_n_id(md_id)).danger
    else:
        d_expression = args.generic(args.fork_n_id(expr_id)).danger

    return d_expression


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attrs = args.graph.nodes[args.n_id]

    if n_attrs.get("expression") == "get" and (
        el_id := search_data_element(args.graph, args.path, args.n_id)
    ):
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(el_id)).danger
        return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)

    d_method = False
    if (
        (metadata_node := args.graph.nodes.get("0"))
        and (lang := decide_language(path=metadata_node["path"]))
        and lang in SUPPORTED_MULTIFILE
    ):
        d_method = evaluate_method_invocation(args, lang)

    d_arguments = False
    if al_id := n_attrs.get("arguments_id"):
        d_arguments = args.generic(args.fork_n_id(al_id)).danger

    d_expression = False
    if expr_id := n_attrs.get("expression_id"):
        d_expression = evaluate_method_expression(args, expr_id)

    d_object = False
    if obj_id := n_attrs.get("object_id"):
        d_object = args.generic(args.fork_n_id(obj_id)).danger

    args.evaluation[args.n_id] = (
        d_expression or d_arguments or d_object or d_method
    )

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
