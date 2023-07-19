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


def java_has_print_statements(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    print_methods = {"print", "println"}
    import_opts = {"System.out", "System.err", "out", "err"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("expression") in print_methods
                and (
                    not (obj_id := graph.nodes[node].get("object_id"))
                    or graph.nodes[obj_id].get("symbol") in import_opts
                )
                and (args_id := graph.nodes[node].get("arguments_id"))
                and g.match_ast_d(
                    graph,
                    args_id,
                    "SymbolLookup",
                    depth=-1,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f237.has_print_statements",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_HAS_PRINT_STATEMENTS,
    )
