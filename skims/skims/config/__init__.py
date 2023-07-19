import confuse
from ctx import (
    STATE_FOLDER,
)
from model import (
    core,
)
import os
from typing import (
    Any,
    Dict,
)
from utils.logs import (
    log_blocking,
)
import yaml


def load_checks(config: Dict[str, Any]) -> set[core.FindingEnum]:
    # All checks by default, or the selected by the checks field
    return (
        {
            core.FindingEnum[finding]
            for finding in config.pop("checks")
            if finding in core.FindingEnum.__members__
        }
        if "checks" in config
        else set(core.FindingEnum)
    )


def load(config_path: str) -> core.SkimsConfig:
    template = confuse.Configuration("skims", read=False)
    template.set_file(config_path)
    template.read(user=False, defaults=False)

    config = template.get(
        confuse.Template(
            {
                "apk": confuse.Template(
                    {
                        "exclude": confuse.Sequence(confuse.String()),
                        "include": confuse.Sequence(confuse.String()),
                    },
                ),
                "checks": confuse.Sequence(confuse.String()),
                "debug": confuse.OneOf([True, False]),
                "commit": confuse.String(),
                "dast": confuse.Template(
                    {
                        "aws_credentials": confuse.Sequence(
                            confuse.Template(
                                {
                                    "access_key_id": confuse.String(),
                                    "secret_access_key": confuse.String(),
                                }
                            )
                        ),
                        "urls": confuse.Sequence(confuse.String()),
                        "ssl_checks": confuse.OneOf([True, False]),
                        "http_checks": confuse.OneOf([True, False]),
                    }
                ),
                "language": confuse.Choice(core.LocalesEnum),
                "multifile": confuse.OneOf([True, False]),
                "namespace": confuse.String(),
                "strict": confuse.OneOf([True, False]),
                "sca": confuse.Template(
                    {
                        "exclude": confuse.Sequence(confuse.String()),
                        "include": confuse.Sequence(confuse.String()),
                    },
                ),
                "output": confuse.Template(
                    {
                        "file_path": confuse.String(),
                        "format": confuse.OneOf(
                            [_format.value for _format in core.OutputFormat]
                        ),
                    }
                ),
                "execution_id": confuse.String(),
                "sast": confuse.Template(
                    {
                        "exclude": confuse.Sequence(confuse.String()),
                        "include": confuse.Sequence(confuse.String()),
                        "lib_path": confuse.OneOf([True, False]),
                        "lib_root": confuse.OneOf([True, False]),
                        "recursion_limit": confuse.Optional(confuse.Integer()),
                    },
                ),
                "working_dir": confuse.String(),
            }
        ),
    )

    try:
        config_apk = config.pop("apk", {})
        config_sast = config.pop("sast", {})
        config_sca = config.pop("sca", {})
        config_dast = config.pop("dast", {}) or {}
        output = config.pop("output", None)

        skims_config = core.SkimsConfig(
            apk=core.SkimsAPKConfig(
                exclude=config_apk.pop("exclude", ()),
                include=config_apk.pop("include", ()),
            ),
            checks=load_checks(config),
            commit=config.pop("commit", None),
            dast=core.SkimsDastConfig(
                aws_credentials=[
                    core.AwsCredentials(
                        access_key_id=cred["access_key_id"],
                        secret_access_key=cred["secret_access_key"],
                    )
                    for cred in config_dast.get("aws_credentials", [])
                ],
                urls=tuple(url for url in config_dast.get("urls", ())),
                http_checks=config_dast.get("http_checks", False),
                ssl_checks=config_dast.get("ssl_checks", False),
            ),
            debug=config.pop("debug", False),
            language=core.LocalesEnum(config.pop("language", "EN")),
            multifile=config.pop("multifile", False),
            namespace=config.pop("namespace"),
            strict=config.pop("strict", False),
            sca=core.SkimsScaConfig(
                exclude=config_sca.pop("exclude", ()),
                include=config_sca.pop("include", ()),
            ),
            output=core.SkimsOutputConfig(
                file_path=os.path.abspath(output["file_path"]),
                format=core.OutputFormat(output["format"]),
            )
            if output
            else None,
            sast=core.SkimsSastConfig(
                exclude=config_sast.pop("exclude", ()),
                include=config_sast.pop("include", ()),
                lib_path=config_sast.pop("lib_path", True),
                lib_root=config_sast.pop("lib_root", True),
                recursion_limit=config_sast.get("recursion_limit", None),
            ),
            start_dir=os.getcwd(),
            working_dir=str(
                os.path.abspath(config.pop("working_dir", "."))
            ).replace("/home/makes/.skims", STATE_FOLDER),
            execution_id=config.pop("execution_id", None),
        )
    except KeyError as exc:
        raise confuse.ConfigError(f"Key: {exc.args[0]} is required")
    else:
        if config:
            unrecognized_keys: str = ", ".join(config)
            if unrecognized_keys == "path":
                log_blocking(
                    "error",
                    (
                        'The "%s" configuration key was renamed.'
                        ' Please use "sast" instead.'
                    ),
                    unrecognized_keys,
                )
                log_blocking(
                    "warning",
                    (
                        "If you are trying to perform your CASA Tier 2"
                        " application security tests see this: "
                        "https://docs.fluidattacks.com/tech/"
                        "scanner/standalone/casa/"
                    ),
                )
            else:
                raise confuse.ConfigError(
                    f"Some keys were not recognized: {unrecognized_keys}",
                )

    log_blocking("debug", "%s", skims_config)

    return skims_config


def dump_to_yaml(config: core.SkimsConfig) -> str:
    return yaml.dump(
        {
            "apk": {
                "exclude": list(config.apk.exclude),
                "include": list(config.apk.include),
            },
            "checks": [check.name for check in config.checks],
            "commit": config.commit,
            "debug": config.debug,
            "dast": {
                "aws_credentials": [
                    {
                        "access_key_id": cred.access_key_id,
                        "secret_access_key": cred.secret_access_key,
                    }
                    for cred in config.dast.aws_credentials
                    if cred
                ],
                "urls": list(config.dast.urls),
                "http_checks": config.dast.http_checks,
                "ssl_checks": config.dast.ssl_checks,
            }
            if config.dast
            else None,
            "language": config.language.value,
            "multifile": config.multifile,
            "namespace": config.namespace,
            "strict": config.strict,
            "sca": {
                "exclude": list(config.sca.exclude),
                "include": list(config.sca.include),
            },
            "output": {
                "file_path": config.output.file_path,
                "format": config.output.format.value,
            }
            if config.output
            else None,
            "execution_id": config.execution_id,
            "sast": {
                "exclude": list(config.sast.exclude),
                "include": list(config.sast.include),
                "lib_path": config.sast.lib_path,
                "lib_root": config.sast.lib_root,
                "recursion_limit": config.sast.recursion_limit,
            },
            "working_dir": config.working_dir,
        }
    )
