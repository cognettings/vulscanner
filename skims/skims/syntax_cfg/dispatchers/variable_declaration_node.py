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
    if m_id := match_ast_d(args.graph, args.n_id, "MethodDeclaration"):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(m_id, args.nxt_id)),
            label_cfg="CFG",
        )

    if args.nxt_id:
        args.graph.add_edge(args.n_id, args.nxt_id, label_cfg="CFG")

    return args.n_id
