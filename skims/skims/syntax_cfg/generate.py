from model.graph import (
    Graph,
    NId,
)
from syntax_cfg.dispatchers import (
    DISPATCHERS,
)
from syntax_cfg.types import (
    MissingCfgBuilder,
    SyntaxCfgArgs,
)
from typing import (
    cast,
)
from utils import (
    logs,
)


def generic(args: SyntaxCfgArgs) -> NId:
    node_type = args.graph.nodes[args.n_id]["label_type"]

    for dispatcher in DISPATCHERS:
        if node_type in dispatcher.applicable_types:
            return dispatcher.cfg_builder(args)

    raise MissingCfgBuilder(f"Missing cfg builder for {node_type}")


def add_syntax_cfg(graph: Graph) -> Graph:
    try:
        generic(args=SyntaxCfgArgs(generic, graph, n_id="1", nxt_id=None))
    except MissingCfgBuilder as error:
        logs.log_blocking("warning", cast(str, error))
    return graph
