from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from fa_purity import (
    JsonObj,
    Maybe,
    Result,
    ResultE,
)
from tap_gitlab import (
    _utils,
)
from tap_gitlab.api._utils import (
    JsonDecodeUtils,
)
from tap_gitlab.api.core.ids import (
    CommitHash,
    RunnerId,
    UserId,
)
from tap_gitlab.api.core.job import (
    Job,
    JobConf,
    JobDates,
    JobId,
    JobResultStatus,
)


@dataclass(frozen=True)
class JobObj:
    job_id: JobId
    obj: Job


def _decode_commit_hash(data: JsonObj) -> ResultE[CommitHash]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_json("commit")
        .map(JsonDecodeUtils)
        .bind(
            lambda j: j.require_str("id")
            .map(CommitHash)
            .alt(
                lambda e: Exception(f"Cannot decode job commit hash. i.e. {e}")
            )
        )
    )


def _decode_job_dates(data: JsonObj) -> ResultE[JobDates]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_str("created_at")
        .bind(_utils.str_to_datetime)
        .bind(
            lambda created_at: _data.get_datetime("started_at").bind(
                lambda started_at: _data.get_datetime("finished_at").map(
                    lambda finished_at: JobDates(
                        created_at, started_at, finished_at
                    )
                )
            )
        )
    ).alt(lambda e: Exception(f"Cannot decode job dates. sub-error: {e}"))


def _decode_job_conf(data: JsonObj) -> ResultE[JobConf]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_bool("allow_failure")
        .bind(
            lambda allow_failure: _data.require_list_of_str("tag_list").bind(
                lambda tag_list: _data.require_str("ref").bind(
                    lambda ref_branch: _data.require_str("stage").map(
                        lambda stage: JobConf(
                            allow_failure,
                            tag_list,
                            ref_branch,
                            stage,
                        )
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job conf. sub-error: {e}"))
    )


def _decode_job_result(data: JsonObj) -> ResultE[JobResultStatus]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_str("status")
        .bind(
            lambda status: _data.get_str("failure_reason").bind(
                lambda failure_reason: _data.get_float("duration")
                .map(lambda m: m.map(Decimal))
                .bind(
                    lambda duration: _data.get_float("queued_duration")
                    .map(lambda m: m.map(Decimal))
                    .map(
                        lambda queued_duration: JobResultStatus(
                            status,
                            failure_reason,
                            duration,
                            queued_duration,
                        )
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job result. sub-error: {e}"))
    )


def _decode_user_id(data: JsonObj) -> ResultE[UserId]:
    _data = JsonDecodeUtils(data)
    return _data.require_json("user").bind(
        lambda user: JsonDecodeUtils(user).require_int("id").map(UserId)
    )


def _decode_runner_id(data: JsonObj) -> ResultE[Maybe[RunnerId]]:
    _data = JsonDecodeUtils(data)
    empty: Maybe[RunnerId] = Maybe.empty()
    return _data.get_generic(
        "runner", lambda u: u.to_json().alt(Exception)
    ).bind(
        lambda m: m.map(
            lambda runner: JsonDecodeUtils(runner)
            .require_int("id")
            .map(RunnerId)
            .map(lambda x: Maybe.from_value(x))
        ).value_or(Result.success(empty))
    )


def _decode_job(data: JsonObj) -> ResultE[Job]:
    _data = JsonDecodeUtils(data)
    return (
        _data.require_str("name")
        .bind(
            lambda name: _decode_user_id(data).bind(
                lambda user: _decode_runner_id(data).bind(
                    lambda runner: _data.get_float("coverage").bind(
                        lambda coverage: _decode_commit_hash(data).bind(
                            lambda commit: _decode_job_dates(data).bind(
                                lambda dates: _decode_job_conf(data).bind(
                                    lambda conf: _decode_job_result(data).map(
                                        lambda result: Job(
                                            name,
                                            user,
                                            runner,
                                            coverage,
                                            commit,
                                            dates,
                                            conf,
                                            result,
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        .alt(lambda e: Exception(f"Cannot decode job. sub-error: {e}"))
    )


def decode_job_id(data: JsonObj) -> ResultE[JobId]:
    return (
        JsonDecodeUtils(data)
        .require_int("id")
        .map(JobId)
        .alt(lambda e: Exception(f"Cannot decode job id. sub-error: {e}"))
    )


def decode_job_obj(data: JsonObj) -> ResultE[JobObj]:
    _id = decode_job_id(data)
    return _id.bind(
        lambda jid: _decode_job(data).map(lambda j: JobObj(jid, j))
    ).alt(lambda e: Exception(f"Cannot decode job obj. sub-error: {e}"))
