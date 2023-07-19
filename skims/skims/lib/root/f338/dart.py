from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.context.search import (
    definition_search,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils.graph import (
    adj_ast,
)


def is_salt_literal(graph: Graph, al_id: NId) -> bool:
    n_id = adj_ast(graph, al_id)[0]
    if graph.nodes[n_id]["label_type"] == "Literal":
        return True

    if graph.nodes[n_id]["label_type"] != "SymbolLookup":
        return False
    searched_symbol = graph.nodes[n_id]["symbol"]
    for path in get_backward_paths(graph, n_id):
        if (
            (var_def := definition_search(graph, path, searched_symbol))
            and graph.nodes[var_def]["label_type"] == "VariableDeclaration"
            and (value_id := graph.nodes[var_def].get("value_id"))
            and graph.nodes[value_id].get("value_type") == "string"
        ):
            return True

    return False


def dart_salting_is_harcoded(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.DART_SALT_IS_HARDCODED
    danger_methods = {"encode", "bytestohex", "fromcharcodes"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if (
                (expr := graph.nodes[n_id].get("expression"))
                and expr.rsplit(".", maxsplit=1)[-1].lower() in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and is_salt_literal(graph, al_id)
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f338.salt_is_hardcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
