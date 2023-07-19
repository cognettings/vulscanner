from collections.abc import (
    Iterator,
)
from lib.root.f089.common import (
    json_parse_unval_data,
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


def json_parse_unvalidated_data(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_JSON_PARSE_UNVALIDATED_DATA

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            f_name = graph.nodes[n_id].get("expression")
            if f_name == "JSON.parse" and json_parse_unval_data(graph, n_id):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f089.parsing_non_validated_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
