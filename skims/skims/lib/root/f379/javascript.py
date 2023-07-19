from collections.abc import (
    Iterator,
)
from lib.root.f379.common import (
    import_is_not_used,
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


def js_import_is_never_used(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_UNNECESSARY_IMPORTS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.graph
        for n_id in import_is_not_used(graph, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f379.unnused_imports",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
