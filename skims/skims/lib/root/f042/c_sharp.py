from collections.abc import (
    Iterator,
)
from lib.root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_insecure_cookie_object(
    method: MethodsEnum,
    graph: Graph,
    object_nid: str,
    method_supplies: MethodSupplies,
) -> NId | None:
    security_props = {"HttpOnly", "Secure"}
    pred = g.pred(graph, object_nid)[0]
    var_name = {graph.nodes[pred].get("variable")}

    sec_access = []
    for nid in yield_syntax_graph_member_access(graph, var_name):
        if graph.nodes[nid].get("member") not in security_props:
            continue
        parent_id = g.pred(graph, nid)[0]
        test_nid = graph.nodes[parent_id].get("value_id")
        sec_access.append(nid)
        if get_node_evaluation_results(
            method, graph, test_nid, set(), graph_db=method_supplies.graph_db
        ):
            return pred

    if len(sec_access) < 2:
        return pred
    return None


def c_sharp_insecurely_generated_cookies(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_COOKIES
    object_name = {"HttpCookie"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") in object_name:
                if pred := is_insecure_cookie_object(
                    method, graph, node, method_supplies
                ):
                    yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.042.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
