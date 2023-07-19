import ctx
from model.core import (
    FindingEnum,
    LocalesEnum,
    SkimsAPKConfig,
    SkimsConfig,
    SkimsDastConfig,
    SkimsSastConfig,
    SkimsScaConfig,
)
import os


def create_test_context(
    include: tuple[str, ...] = (),
    exclude: tuple[str, ...] = (),
) -> None:
    ctx.SKIMS_CONFIG = SkimsConfig(
        apk=SkimsAPKConfig(
            exclude=(),
            include=(),
        ),
        checks=set(FindingEnum),
        commit=None,
        dast=SkimsDastConfig(
            aws_credentials=[],
            urls=(),
            http_checks=False,
            ssl_checks=False,
        ),
        debug=False,
        language=LocalesEnum.EN,
        multifile=False,
        namespace="test",
        strict=False,
        sca=SkimsScaConfig(
            exclude=(),
            include=(),
        ),
        output=None,
        sast=SkimsSastConfig(
            include=include,
            exclude=exclude,
            lib_path=True,
            lib_root=True,
            recursion_limit=None,
        ),
        start_dir=os.getcwd(),
        working_dir=os.getcwd(),
        execution_id="123456789",
    )
