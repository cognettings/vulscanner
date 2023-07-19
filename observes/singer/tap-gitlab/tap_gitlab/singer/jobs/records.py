from dataclasses import (
    dataclass,
)
from fa_purity import (
    FrozenDict,
    PureIter,
    UnfoldedJVal,
)
from fa_purity.json.factory import (
    from_unfolded_dict,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    pure_map,
)
from fa_purity.pure_iter.transform import (
    chain,
)
from fa_singer_io.singer import (
    SingerRecord,
)
from tap_gitlab.api.core.ids import (
    PipelineId,
    ProjectId,
)
from tap_gitlab.api.jobs import (
    JobObj,
)
from tap_gitlab.singer._core import (
    SingerStreams,
)


def job_encode(
    project: ProjectId,
    pipeline: PipelineId,
    job_obj: JobObj,
) -> PureIter[SingerRecord]:
    def _encode_job_tag(tag: str) -> FrozenDict[str, UnfoldedJVal]:
        return FrozenDict(
            {
                "job_id": job_obj.job_id.job_id,
                "project_id": project.str_val,
                "tag": tag,
            }
        )

    _encoded_job_obj: FrozenDict[str, UnfoldedJVal] = FrozenDict(
        {
            "job_id": job_obj.job_id.job_id,
            "project_id": project.str_val,
            "pipe_id": pipeline.global_id,
            "name": job_obj.obj.name,
            "user_id": job_obj.obj.user_id.user_id,
            "runner_id": job_obj.obj.runner_id.map(
                lambda i: i.runner_id
            ).value_or(None),
            "coverage": job_obj.obj.coverage.value_or(None),
            "commit": job_obj.obj.commit.hash_str,
            "created_at": job_obj.obj.dates.created_at.isoformat(),
            "started_at": job_obj.obj.dates.started_at.map(
                lambda d: d.isoformat()
            ).value_or(None),
            "finished_at": job_obj.obj.dates.finished_at.map(
                lambda d: d.isoformat()
            ).value_or(None),
            "allow_failure": job_obj.obj.conf.allow_failure,
            "ref_branch": job_obj.obj.conf.ref_branch,
            "stage": job_obj.obj.conf.stage,
            "status": job_obj.obj.result.status,
            "failure_reason": job_obj.obj.result.failure_reason.value_or(None),
            "duration": job_obj.obj.result.duration.value_or(None),
            "queued_duration": job_obj.obj.result.queued_duration.value_or(
                None
            ),
        }
    )

    encoded_obj = SingerRecord(
        SingerStreams.jobs.value,
        from_unfolded_dict(_encoded_job_obj),
        None,
    )
    job_tags = pure_map(
        lambda t: _encode_job_tag(t), job_obj.obj.conf.tag_list
    ).map(
        lambda d: SingerRecord(
            SingerStreams.job_tags.value, from_unfolded_dict(d), None
        )
    )
    records = (
        from_flist((encoded_obj,)),
        job_tags,
    )
    return chain(from_flist(records))
