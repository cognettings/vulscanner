from collections.abc import (
    Iterator,
)
from lib.root.f188.common import (
    has_dangerous_param,
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


def js_lack_of_validation_dom_window(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JSX_LACK_OF_VALIDATION_EVENT_LISTENER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if has_dangerous_param(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f188.lack_of_data_validation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
