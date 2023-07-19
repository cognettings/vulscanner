from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
    get_optional_attribute,
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
from utils.graph import (
    adj_ast,
)


def _compose_read_only(graph: Graph, nid: NId) -> Iterator[NId]:
    for c_id in adj_ast(graph, graph.nodes[nid]["value_id"]):
        props = graph.nodes[c_id]["value_id"]
        if read := get_optional_attribute(graph, props, "read_only"):
            if read[1].lower() != "true":
                yield read[2]
        else:
            yield c_id


def docker_compose_read_only(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.DOCKER_COMPOSE_READ_ONLY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        if not shard.path.split(".")[-2].endswith("docker-compose"):
            return

        for nid in method_supplies.selected_nodes:
            if serv := get_optional_attribute(graph, nid, "services"):
                for c_id in _compose_read_only(graph, serv[2]):
                    yield shard, c_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f418.docker_compose_read_only",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
