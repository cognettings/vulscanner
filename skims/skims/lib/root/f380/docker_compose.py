from collections.abc import (
    Iterator,
)
from lib.root.utilities.docker import (
    get_key_value,
    validate_path,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def _compose_image_has_digest(value: str, nid: NId) -> Iterator[NId]:
    env_var_re: re.Pattern = re.compile(r"\{.+\}")
    digest_re: re.Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    if not (env_var_re.search(value) or digest_re.search(value)):
        yield nid


def docker_compose_image_has_digest(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.DOCKER_COMPOSE_IMAGE_HAS_DIGEST

    def n_ids() -> Iterator[GraphShardNode]:
        if not validate_path(shard.path):
            return
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            key, value = get_key_value(graph, nid)
            if key == "image":
                for report in _compose_image_has_digest(value, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f380.bash_image_has_digest",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
