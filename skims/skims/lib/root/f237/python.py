from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def python_has_print_statements(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_expr = graph.nodes[n_id].get("expression")
            if (
                n_expr == "print"
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and g.match_ast_d(graph, al_id, "SymbolLookup", depth=-1)
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.PYTHON_HAS_PRINT_STATEMENTS,
    )
