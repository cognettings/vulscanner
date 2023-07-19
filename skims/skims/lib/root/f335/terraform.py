from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_optional_attribute,
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


def tfm_s3_bucket_versioning_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_S3_VERSIONING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name") == "aws_s3_bucket_versioning"
                and (
                    ver_conf := get_argument(
                        graph, nid, "versioning_configuration"
                    )
                )
                and (
                    status := get_optional_attribute(graph, ver_conf, "status")
                )
                and status[1].lower() in {"disabled", "suspended"}
            ):
                yield shard, status[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f335.cfn_s3_bucket_versioning_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
