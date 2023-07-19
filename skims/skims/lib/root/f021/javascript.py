from collections.abc import (
    Iterator,
)
from lib.root.f021.common import (
    insecure_dynamic_xpath,
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


def js_dynamic_xpath(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_DYNAMIC_X_PATH

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in insecure_dynamic_xpath(graph, method, method_supplies):
            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
