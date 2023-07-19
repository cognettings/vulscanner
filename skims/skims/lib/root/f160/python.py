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


def python_unsafe_temp_file(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_UNSAFE_TEMP_FILE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'
            if expr == "tempfile.mktemp":
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f160.insecure_temp_file",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
