from collections.abc import (
    Iterator,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)


def search(args: SearchArgs) -> Iterator[SearchResult]:
    assign_id = args.graph.nodes[args.n_id]["variable_id"]

    if args.symbol == args.graph.nodes[assign_id].get("symbol"):
        yield True, args.n_id
    elif (
        expr := args.graph.nodes[assign_id].get("expression")
    ) and args.symbol in expr:
        yield False, args.n_id
    elif args.graph.nodes[assign_id]["label_type"] == "ElementAccess":
        arg_id = args.graph.nodes[assign_id]["arguments_id"]
        if (val := args.graph.nodes[arg_id].get("value")) and val[
            1:-1
        ] == args.symbol:
            yield True, args.n_id
