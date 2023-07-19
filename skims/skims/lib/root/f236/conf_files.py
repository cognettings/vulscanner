from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    get_key_value,
    is_parent,
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


def _sourcemap_enabled(
    graph: Graph, nid: NId, key_pair: str, value: str
) -> bool:
    if key_pair == "sourceMap" and value.lower() == "true":
        tsconfig_correct_parents = ["compilerOptions"]
        angular_vuln_parents_path = ["production", "configurations", "build"]
        if is_parent(graph, nid, tsconfig_correct_parents):
            return True
        if is_parent(graph, nid, angular_vuln_parents_path):
            return True
    if key_pair == "sourceMaps" and value.lower() == "true":
        serverless_correct_parents = ["configurations"]
        if is_parent(graph, nid, serverless_correct_parents):
            return True
    return False


def tsconfig_sourcemap_enabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TSCONFIG_SOURCEMAP_ENABLED

    def n_ids() -> Iterator[GraphShardNode]:
        if shard.path.endswith("tsconfig.spec.json"):
            return
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key, value = get_key_value(graph, nid)

            if _sourcemap_enabled(graph, nid, key, value):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f236.tsconfig_sourcemap_enabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
