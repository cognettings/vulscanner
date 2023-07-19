from collections.abc import (
    Iterator,
)
from lib.root.f004.common import (
    remote_command_exec_nodes,
)
from model import (
    core,
)
from model.core import (
    MethodsEnum,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def ts_remote_command_execution(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> core.Vulnerabilities:
    method = MethodsEnum.TS_REMOTE_COMMAND_EXECUTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in remote_command_exec_nodes(graph, method, method_supplies):
            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f004.remote_command_execution",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
