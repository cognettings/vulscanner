from concurrent.futures import (
    Future,
    wait,
)
from concurrent.futures.process import (
    ProcessPoolExecutor,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
import ctx
from functools import (
    partial,
)
from lib.root import (
    QUERIES,
)
from model import (
    core,
)
from model.core import (
    SkimsConfig,
    Vulnerabilities,
    Vulnerability,
)
from model.graph import (
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage,
    MethodSupplies,
)
import os
from sast.parse import (
    get_graph_db,
    get_shard,
)
from schedulers.report import (
    send_vulnerability_to_sqs,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Callable,
)
from utils.fs import (
    decide_language,
)
from utils.graph import (
    nodes_by_type,
)


def _store_results_callback(
    stores: dict[core.FindingEnum, EphemeralStore],
    future: Future,
) -> None:
    with suppress(Exception):
        results: tuple[Vulnerability, ...] = future.result()
        for result in results:
            stores[result.finding].store(result)
            send_vulnerability_to_sqs(result)


def analyze(
    *,
    stores: dict[core.FindingEnum, EphemeralStore],
    paths: tuple[str, ...],
) -> None:
    has_failed = False
    executor = (
        ThreadPoolExecutor
        if ctx.SKIMS_CONFIG.multifile
        else ProcessPoolExecutor
    )
    with executor(
        max_workers=os.cpu_count(),
    ) as worker:
        graph_db = (
            get_graph_db(
                paths, ctx.SKIMS_CONFIG.working_dir, ctx.SKIMS_CONFIG.debug
            )
            if ctx.SKIMS_CONFIG.multifile
            else None
        )
        for path in paths:
            futures: list = []
            futures = get_futures(
                graph_db=graph_db,
                path=path,
                lang=decide_language(path),
                futures=futures,
                stores=stores,
                worker=worker,
            )
            _, f_failed = wait(futures, 60)
            if f_failed and not has_failed:
                has_failed = True
        check_failure(worker, has_failed)


def get_futures(
    *,
    graph_db: GraphDB | None,
    path: str,
    lang: GraphShardMetadataLanguage,
    futures: list,
    stores: dict[core.FindingEnum, EphemeralStore],
    worker: ThreadPoolExecutor | ProcessPoolExecutor,
) -> list:
    if not ((graph_db) and (shard := graph_db.shards_by_path_f(path))):
        shard = get_shard(
            path, lang, ctx.SKIMS_CONFIG.working_dir, ctx.SKIMS_CONFIG.debug
        )

    if not shard or not shard.syntax_graph:
        return futures
    for label, nodes in nodes_by_type(shard.syntax_graph).items():
        if queries_node := QUERIES[lang].get(label):
            for finding, query in queries_node:
                if finding in ctx.SKIMS_CONFIG.checks:
                    future = worker.submit(
                        _analyze_one,
                        config=ctx.SKIMS_CONFIG,
                        query=query,
                        shard=shard,
                        method_supplies=MethodSupplies(nodes, graph_db),
                    )
                    future.add_done_callback(
                        partial(_store_results_callback, stores)
                    )
                    futures.append(future)
    return futures


def _analyze_one(
    config: SkimsConfig,
    query: Callable[[GraphShard, MethodSupplies], Vulnerabilities],
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    # Re-export config to gain visibility in child subprocesses
    ctx.SKIMS_CONFIG = config

    return query(
        shard,
        method_supplies,
    )


def check_failure(
    worker: ThreadPoolExecutor | ProcessPoolExecutor, has_failed: bool
) -> None:
    if isinstance(worker, ProcessPoolExecutor) and has_failed:
        for (
            process
        ) in worker._processes.values():  # pylint: disable=protected-access
            process.kill()
    elif isinstance(worker, ThreadPoolExecutor) and has_failed:
        worker.shutdown(wait=False, cancel_futures=True)
