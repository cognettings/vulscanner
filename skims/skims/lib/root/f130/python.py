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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)


def python_secure_cookie(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_SECURE_COOKIE
    danger_set = {
        "set_cookie",
        "AuthTktCookieHelper",
        "AuthTktAuthenticationPolicy",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            expr = graph.nodes[n_id]["expression"].split(".")
            if (
                expr[-1] in danger_set
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and get_node_evaluation_results(method, graph, al_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f130.set_cookie_set_secure",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
