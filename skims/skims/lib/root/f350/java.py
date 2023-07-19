from collections.abc import (
    Iterator,
)
from lib.root.utilities.java import (
    concatenate_name,
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


def use_insecure_trust_manager(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_TRUST_MANAGER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            m_name = concatenate_name(graph, n_id)
            m_split = m_name.lower().split(".")
            if (
                m_split[0] == "sslcontextbuilder"
                and m_split[-1] == "trustmanager"
                and get_node_evaluation_results(method, graph, n_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f350.insecure_trust_manager",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
