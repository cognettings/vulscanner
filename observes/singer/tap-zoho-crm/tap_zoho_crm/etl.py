from fa_purity import (
    Cmd,
    FrozenDict,
)
from fa_purity.cmd import (
    CmdUnwrapper,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json_2 import (
    JsonObj,
    JsonPrimitive,
    JsonValue,
    LegacyAdapter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from fa_singer_io.singer import (
    emitter,
    SingerRecord,
)
import logging
from redshift_client.sql_client import (
    new_client,
    SqlClient,
)
from redshift_client.sql_client.connection import (
    Credentials as DbCredentials,
    DatabaseId,
    DbConnection,
    IsolationLvl,
)
import sys
from tap_zoho_crm import (
    core,
    db,
)
from tap_zoho_crm.api import (
    ApiClientFactory,
)
from tap_zoho_crm.api.auth import (
    Credentials,
)
from tap_zoho_crm.api.bulk import (
    BulkData,
    BulkJob,
    BulkJobId,
    ModuleName,
)
from tap_zoho_crm.api.common import (
    PageIndex,
)
from tap_zoho_crm.api.users import (
    UsersDataPage,
    UserType,
)
from tap_zoho_crm.core import (
    CoreClient,
    IBulk as BulkUtils,
)
import tempfile
from typing import (
    Dict,
    FrozenSet,
)

ALL_MODULES = frozenset(ModuleName)
LOG = logging.getLogger(__name__)


class MissingModuleData(Exception):
    pass


def _core_client(crm_creds: Credentials, client: SqlClient) -> Cmd[CoreClient]:
    return ApiClientFactory.new_client(crm_creds).map(
        lambda api: core.new_client(api, db.new_job_client(client))
    )


def initialize(
    db_id: DatabaseId,
    db_creds: DbCredentials,
) -> Cmd[None]:
    return DbConnection.connect_and_execute(
        db_id,
        db_creds,
        False,
        IsolationLvl.READ_COMMITTED,
        True,
        lambda c: new_client(c, LOG).bind(db.init_db),
    )


def creation_phase(
    crm_creds: Credentials,
    db_id: DatabaseId,
    db_creds: DbCredentials,
    target_modules: FrozenSet[ModuleName] = ALL_MODULES,
) -> Cmd[None]:
    """Creates bulk jobs for the `target_modules`"""

    def _create(core: CoreClient) -> Cmd[None]:
        triggered_modules = core.bulk.get_all.map(
            lambda f: from_flist(tuple(f))
            .map(lambda j: j.job.module)
            .transform(lambda x: frozenset(x))
        )
        diff = triggered_modules.bind(
            lambda triggered: from_flist(tuple(target_modules - triggered))
            .map(lambda m: core.bulk.create(m, 1))
            .transform(consume)
        )
        return core.bulk.update_all + diff

    return DbConnection.connect_and_execute(
        db_id,
        db_creds,
        False,
        IsolationLvl.READ_COMMITTED,
        True,
        lambda c: new_client(c, LOG).bind(
            lambda sql: _core_client(crm_creds, sql).bind(_create),
        ),
    )


def _get_completed_jobs_map(
    bulk_utils: BulkUtils,
) -> Cmd[FrozenDict[BulkJobId, BulkJob]]:
    return bulk_utils.update_all + bulk_utils.get_all.map(
        lambda f: from_flist(tuple(f))
        .filter(lambda j: j.job.state.upper() == "COMPLETED")
        .map(lambda j: (j.job_id, j.job))
        .transform(lambda i: freeze(dict(i)))
    )


def _emit_bulk_data(
    id_job_map: FrozenDict[BulkJobId, BulkJob], data: BulkData
) -> Cmd[None]:
    def _action(unwrap: CmdUnwrapper) -> None:
        with tempfile.NamedTemporaryFile(
            "w+", delete=False
        ) as persistent_file:
            data.file.seek(0)
            persistent_file.write(data.file.read())
            module_name: str = id_job_map[data.job_id].module.value
            options: Dict[str, JsonValue] = {
                "quote_nonnum": JsonValue.from_primitive(
                    JsonPrimitive.from_bool(True)
                ),
                "add_default_types": JsonValue.from_primitive(
                    JsonPrimitive.from_bool(True)
                ),
                "pkeys_present": JsonValue.from_primitive(
                    JsonPrimitive.from_bool(False)
                ),
                "only_records": JsonValue.from_primitive(
                    JsonPrimitive.from_bool(True)
                ),
            }
            raw: Dict[str, JsonValue] = {
                "csv_path": JsonValue.from_primitive(
                    JsonPrimitive.from_str(persistent_file.name)
                ),
                "options": JsonValue.from_json(
                    freeze(options),
                ),
            }
            record = SingerRecord(
                module_name, LegacyAdapter.to_legacy_json(freeze(raw)), None
            )
            unwrap.act(emitter.emit(sys.stdout, record))

    return Cmd.new_cmd(_action)


def _emit_bulk_data_set(
    data: FrozenSet[BulkData],
    id_job_map: FrozenDict[BulkJobId, BulkJob],
) -> Cmd[None]:
    return (
        from_flist(tuple(data))
        .map(lambda x: _emit_bulk_data(id_job_map, x))
        .transform(consume)
    )


def _emit_user_data(data: UsersDataPage) -> Cmd[None]:
    def _emit(user_data: JsonObj) -> Cmd[None]:
        record = SingerRecord(
            "users", LegacyAdapter.to_legacy_json(user_data), None
        )
        return emitter.emit(sys.stdout, record)

    return from_flist(tuple(data.data)).map(_emit).transform(consume)


def _extraction_phase(
    core_api: CoreClient, completed: FrozenDict[BulkJobId, BulkJob]
) -> Cmd[None]:
    ready_modules = (
        from_flist(tuple(completed.values()))
        .map(lambda x: x.module)
        .transform(lambda x: frozenset(x))
    )
    missing = ALL_MODULES - ready_modules
    if missing:
        raise MissingModuleData(str(missing))
    data = core_api.bulk.extract_data(frozenset(completed.keys())).bind(
        lambda d: _emit_bulk_data_set(d, completed)
    )
    users_data = core_api.users.get_users(
        UserType.ANY, PageIndex(1, 200)
    ).bind(_emit_user_data)
    return data + users_data


def start_streamer(
    crm_creds: Credentials, db_id: DatabaseId, db_creds: DbCredentials
) -> Cmd[None]:
    return DbConnection.connect_and_execute(
        db_id,
        db_creds,
        False,
        IsolationLvl.READ_COMMITTED,
        True,
        lambda c: new_client(c, LOG).bind(
            lambda sql: _core_client(crm_creds, sql).bind(
                lambda core: _get_completed_jobs_map(core.bulk).bind(
                    lambda j: _extraction_phase(core, j)
                )
            )
        ),
    )
