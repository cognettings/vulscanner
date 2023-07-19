from collections.abc import (
    Iterator,
)
from lib.root.f128.common import (
    insecure_cookies,
)
from lib.root.utilities.javascript import (
    file_imports_module,
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


def js_insecure_cookies(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_COOKIE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        if not file_imports_module(graph, "ngx-cookie-service"):
            return
        for n_id in method_supplies.selected_nodes:
            if insecure_cookies(graph, n_id):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f128.set_cookie_missing_httponly",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
