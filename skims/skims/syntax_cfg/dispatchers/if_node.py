from model.graph import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs) -> NId:
    if true_id := args.graph.nodes[args.n_id].get("true_id"):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(true_id, args.nxt_id)),
            label_cfg="CFG",
        )

    if false_id := args.graph.nodes[args.n_id].get("false_id"):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(false_id, args.nxt_id)),
            label_cfg="CFG",
        )

    if args.nxt_id:
        args.graph.add_edge(args.n_id, args.nxt_id, label_cfg="CFG")

    return args.n_id
