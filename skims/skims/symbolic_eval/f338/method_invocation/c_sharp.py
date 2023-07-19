from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.context.search import (
    definition_search,
)
from symbolic_eval.types import (
    Path,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)


def is_salt_literal(graph: Graph, path: Path, n_id: NId) -> bool:
    if graph.nodes[n_id]["label_type"] == "Literal":
        return True

    if graph.nodes[n_id]["label_type"] != "SymbolLookup":
        return False
    searched_symbol = graph.nodes[n_id]["symbol"]
    if (
        (var_def := definition_search(graph, path, searched_symbol))
        and graph.nodes[var_def]["label_type"] == "VariableDeclaration"
        and (value_id := graph.nodes[var_def].get("value_id"))
        and graph.nodes[value_id].get("value_type") == "string"
    ):
        return True
    return False


def cs_check_hashes_salt(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    ma_attr = args.graph.nodes[args.n_id]
    if (
        ma_attr["expression"].rsplit(".", maxsplit=1)[-1] == "GetBytes"
        and (args_id := ma_attr.get("arguments_id"))
        and (args_nids := adj_ast(args.graph, args_id))
        and len(args_nids) == 1
        and is_salt_literal(args.graph, args.path, args_nids[0])
    ):
        args.triggers.add("hardcode_salt")
        args.evaluation[args.n_id] = True
    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
