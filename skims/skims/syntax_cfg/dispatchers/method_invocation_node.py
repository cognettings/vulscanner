from model.graph import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)
from utils.graph import (
    match_ast_d,
)


def build(args: SyntaxCfgArgs) -> NId:
    al_id = args.graph.nodes[args.n_id].get("arguments_id")
    if al_id and match_ast_d(args.graph, al_id, "MethodDeclaration"):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(al_id, args.nxt_id)),
            label_cfg="CFG",
        )

    if args.nxt_id:
        args.graph.add_edge(args.n_id, args.nxt_id, label_cfg="CFG")

    return args.n_id
