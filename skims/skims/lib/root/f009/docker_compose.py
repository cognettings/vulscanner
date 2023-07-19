from collections.abc import (
    Iterator,
)
from lib.path.f009.utils import (
    is_key_sensitive,
)
from lib.root.utilities.docker import (
    iterate_env_variables,
    validate_path,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def _compose_env_secrets(graph: Graph, nid: NId) -> Iterator[NId]:
    secret_smells: set[str] = {
        "api_key",
        "jboss_pass",
        "license_key",
        "password",
        "secret",
    }
    env_var = graph.nodes[nid]["value"]
    env_var_str: str = env_var.lower()
    key_val = env_var_str.split("=", 1)
    secret = key_val[0]
    value = key_val[1].strip("'").strip('"') if len(key_val) > 1 else None
    if (
        (
            any(smell in secret for smell in secret_smells)
            or is_key_sensitive(secret)
        )
        and value
        and not (value.startswith("${") and value.endswith("}"))
    ):
        yield nid


def docker_compose_env_secrets(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.DOCKER_COMPOSE_ENV_SECRETS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        if shard.syntax_graph is None or not validate_path(shard.path):
            return
        for nid in iterate_env_variables(graph, method_supplies):
            for report in _compose_env_secrets(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f009.docker_compose_env_secrets",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
