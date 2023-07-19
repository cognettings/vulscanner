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


def is_salt_arg_literal(
    graph: Graph, args_ids: tuple[NId, ...], name: str
) -> bool:
    n_id = args_ids[0]
    if name == "PBEKeySpec":
        n_id = args_ids[1]

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


def kt_salting_is_harcoded(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KOTLIN_SALT_IS_HARDCODED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs.get("expression") in {"PBEKeySpec", "PBEParameterSpec"}
                and (al_id := n_attrs.get("arguments_id"))
                and (args_nids := adj_ast(graph, al_id))
                and len(args_nids) >= 1
                and is_salt_arg_literal(
                    graph, args_nids, n_attrs["expression"]
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f338.salt_is_hardcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
