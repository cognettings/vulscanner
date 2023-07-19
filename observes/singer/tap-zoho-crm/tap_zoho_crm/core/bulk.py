from fa_purity import (
    Cmd,
    PureIter,
)
from fa_purity.cmd.transform import (
    serial_merge,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
import logging
from tap_zoho_crm.api.bulk import (
    BulkData,
    BulkJobApi,
    BulkJobId,
    BulkJobObj,
    ModuleName,
)
from tap_zoho_crm.db import (
    Client as DbClient,
)
from typing import (
    FrozenSet,
    Tuple,
)

LOG = logging.getLogger(__name__)


def create_bulk_job(
    api_client: BulkJobApi, db_client: DbClient, module: ModuleName, page: int
) -> Cmd[None]:
    """Creates bulk job on crm and stores it on DB"""
    return api_client.new(module, page).bind(
        lambda job: db_client.save_bulk_job(job)
    )


def update_all(api_client: BulkJobApi, db_client: DbClient) -> Cmd[None]:
    """
    Get the updated status of the jobs (from crm) and update them in the DB
    """

    def _update_jobs(
        db_jobs: PureIter[BulkJobObj], updated_jobs: PureIter[BulkJobObj]
    ) -> Cmd[None]:
        current_status = db_jobs.map(
            lambda j: (j.job_id, j.job.state)
        ).transform(lambda x: frozenset(x))
        updated_status = updated_jobs.map(
            lambda j: (j.job_id, j.job.state)
        ).transform(lambda x: frozenset(x))
        need_update: FrozenSet[Tuple[BulkJobId, str]] = (
            updated_status - current_status
        )
        need_update_ids: FrozenSet[BulkJobId] = frozenset(
            [_id for _id, _ in need_update]
        )
        msg = Cmd.from_cmd(
            lambda: LOG.info("Updating %s jobs status", len(need_update))
        )
        update = (
            updated_jobs.filter(lambda job: job.job_id in need_update_ids)
            .map(db_client.update_bulk_job)
            .transform(lambda x: serial_merge(x.to_list()))
            .map(lambda _: None)
        )
        return msg + update

    def _action(db_jobs: PureIter[BulkJobObj]) -> Cmd[None]:
        updated_jobs = (
            db_jobs.map(
                lambda job: api_client.get(job.job_id).map(
                    lambda j: BulkJobObj(job.job_id, j)
                )
            )
            .transform(lambda i: serial_merge(i.to_list()))
            .map(lambda x: from_flist(x))
        )
        return updated_jobs.bind(lambda u: _update_jobs(db_jobs, u))

    return db_client.get_bulk_jobs.bind(
        lambda i: _action(from_flist(tuple(frozenset(i))))
    )


def get_bulk_data(
    client: BulkJobApi, jobs_id: FrozenSet[BulkJobId]
) -> Cmd[FrozenSet[BulkData]]:
    return (
        from_flist(tuple(jobs_id))
        .map(client.download)
        .transform(lambda i: serial_merge(i.to_list()))
        .map(frozenset)
    )
