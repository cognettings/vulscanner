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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def is_plain_text_credentials(graph: Graph, n_id: NId) -> bool:
    args_ids = g.adj_ast(graph, n_id)
    if len(args_ids) < 2:
        return False

    for _id in args_ids[1:]:
        n_attrs = graph.nodes[_id]
        if n_attrs["label_type"] == "Literal":
            return True
    return False


def c_sharp_plain_text_keys(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.C_SHARP_PLAIN_TEXT_KEYS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            m_name = n_attrs["expression"].split(".")[-1]
            if (
                m_name == "decrypt"
                and (al_id := n_attrs.get("arguments_id"))
                and is_plain_text_credentials(graph, al_id)
                and get_node_evaluation_results(
                    method, graph, n_attrs["expression_id"], {"cryptlib"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f169.plain_text_keys",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
