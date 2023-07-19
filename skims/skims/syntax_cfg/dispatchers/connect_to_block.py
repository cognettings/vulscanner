from model.graph import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs) -> NId:
    if block_id := args.graph.nodes[args.n_id].get("block_id"):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(block_id, args.nxt_id)),
            label_cfg="CFG",
        )
    return args.n_id
