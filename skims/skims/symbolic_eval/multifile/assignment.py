from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.context.search import (
    definition_search,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
)
import sympy
from utils import (
    graph as g,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def get_node_to_evaluate(
    args: SymbolicEvalArgs,
) -> tuple[NId | None, NId | None]:
    invalid_operators = {"&&"}

    if (
        (pred := g.pred_ast(args.graph, args.n_id))
        and args.graph.nodes[pred[0]]["label_type"] == "If"
        and (condition_node := args.graph.nodes[pred[0]]["condition_id"])
        and args.graph.nodes[condition_node]["operator"]
        not in invalid_operators
    ):
        return condition_node, pred[0]
    if (
        ternary := g.match_ast_d(args.graph, args.n_id, "TernaryOperation")
    ) and (condition_node := args.graph.nodes[ternary].get("condition_id")):
        return condition_node, ternary
    return None, None


def evaluate_if_statement(args: SymbolicEvalArgs) -> NId | None:
    var_types = {"decimal_integer_literal"}

    condition_node, statement_node = get_node_to_evaluate(args)

    if condition_node and statement_node:
        variables = get_variables(args, condition_node, [])

        path = args.graph.nodes["0"]["path"]

        if (
            args.graph_db
            and (shard := args.graph_db.shards_by_path_f(path))
            and (ast_graph := shard.graph)
        ):
            for var in variables:
                if (
                    (val_id := get_var_value_id(args, var))
                    and ast_graph.nodes[val_id]["label_type"] in var_types
                    and (
                        var_value := ast_graph.nodes[val_id].get("label_text")
                    )
                ):
                    ast_graph.nodes[var]["label_text"] = var_value
            get_evaluation_result(
                ast_graph, args.graph, condition_node, statement_node
            )
            return statement_node
    return None


def get_evaluation_result(
    ast_graph: Graph, syntax_graph: Graph, condition_node: NId, if_node: NId
) -> None:
    result = sympy.simplify(node_to_str(ast_graph, condition_node))

    if isinstance(result, sympy.logic.boolalg.BooleanTrue) and (
        true_id := syntax_graph.nodes[if_node].get("true_id")
    ):
        syntax_graph.nodes[if_node]["execution_node"] = true_id
    elif isinstance(result, sympy.logic.boolalg.BooleanFalse) and (
        false_id := syntax_graph.nodes[if_node].get("false_id")
    ):
        syntax_graph.nodes[if_node]["execution_node"] = false_id


def get_variables(
    args: SymbolicEvalArgs, n_id: NId, symbols: list[NId]
) -> list[NId]:
    if args.graph.nodes[n_id]["label_type"] == "SymbolLookup":
        symbols.append(n_id)
    else:
        for node in g.adj_ast(args.graph, n_id):
            get_variables(args, node, symbols)
    return symbols


def get_var_value_id(args: SymbolicEvalArgs, n_id: NId) -> NId | None:
    if (
        (
            var_definition := definition_search(
                args.graph, args.path, args.graph.nodes[n_id]["symbol"]
            )
        )
        and args.graph.nodes[var_definition]["label_type"]
        == "VariableDeclaration"
        and (value_id := args.graph.nodes[var_definition].get("value_id"))
    ):
        return value_id
    return None
