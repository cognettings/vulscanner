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
from symbolic_eval.utils import (
    get_value_member_access,
)
import utils.graph as g


def c_sharp_disabled_http_header_check(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_DISABLED_HTTP_HEADER_CHECK

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("name") == "HttpRuntimeSection"
                and (pred := g.pred_ast(graph, node)[0])
                and graph.nodes[pred].get("label_type")
                == "VariableDeclaration"
            ):
                ident = graph.nodes[pred].get("variable")
                if (
                    value := get_value_member_access(
                        graph, ident, "EnableHeaderChecking"
                    )
                ) and graph.nodes[value].get("value") == "false":
                    yield shard, value

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f414.disabled_http_header_check",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
