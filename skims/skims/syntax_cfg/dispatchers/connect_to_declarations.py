from model.graph import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)
from utils.graph import (
    match_ast,
)

DEC_TYPES = {"Class", "MethodDeclaration"}


def build(args: SyntaxCfgArgs) -> NId:
    childs = match_ast(args.graph, args.n_id, "Class", "MethodDeclaration")
    child_ids = filter(
        None, [childs.get(label_type) for label_type in DEC_TYPES]
    )

    for _id in child_ids:
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(_id, args.nxt_id)),
            label_cfg="CFG",
        )

    return args.n_id
