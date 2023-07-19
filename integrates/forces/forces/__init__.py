"""Fluidattacks Forces package."""

from aioextensions import (
    in_thread,
)
from forces.apis.git import (
    check_remotes,
    get_repository_metadata,
)
from forces.apis.integrates import (
    set_api_token,
)
from forces.apis.integrates.api import (
    upload_report,
)
from forces.model import (
    ForcesConfig,
    ForcesReport,
    KindEnum,
    StatusCode,
)
from forces.report import (
    format_forces_report,
)
from forces.report.data import (
    compile_raw_report,
)
from forces.utils.function import (
    remove_color_codes,
)
from forces.utils.logs import (
    CONSOLE_INTERFACE,
    log,
    LOG_FILE,
    rich_log,
)
from forces.utils.strict_mode import (
    set_forces_exit_code,
)
import os
import uuid


async def entrypoint(
    token: str,
    config: ForcesConfig,
) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()
    exit_code: int = 0
    set_api_token(token)

    metadata = await in_thread(
        get_repository_metadata,
        repo_path=config.repository_path,
    )
    metadata["git_repo"] = config.repository_name or metadata["git_repo"]
    with CONSOLE_INTERFACE.status(
        "[bold green]Working on reports...[/]", spinner="aesthetic"
    ):
        tasks: dict[str, str] = {
            "gathering": "Gathering findings data",
            "processing": "Processing findings data",
            "formatting": "Formatting findings data",
            "uploading": "Uploading Report to ARM",
        }
        footer: str = ": [green]Complete[/]"
        if config.repository_name:
            await log(
                "info",
                (
                    f"Looking for {config.kind} vulnerabilities "
                    f"associated with the repo: "
                    f"[bright_yellow]{config.repository_name}[/] "
                    f"of group {config.group}."
                ),
            )
            if config.kind != KindEnum.STATIC:
                await log(
                    "info",
                    (
                        "Dynamic vulnerabilities in this group not associated "
                        "with any repositories will also be included in the "
                        "report"
                    ),
                )
            # check if repo is in roots
            if config.kind != KindEnum.ALL and not await check_remotes(config):
                return StatusCode.ERROR
        else:
            await log(
                "warning",
                (
                    "No specific repository name has been set. "
                    "Looking for vulnerabilities in [bright_yellow]all[/] "
                    f"repositories registered in {config.group}"
                ),
            )

        await log("info", f"{tasks['gathering']}{footer}")
        report = await compile_raw_report(config)

        if (
            config.verbose_level == 2 and report.summary.vulnerable.total > 0
        ) or not report.summary.group_compliance:
            await log("info", f"{tasks['processing']}{footer}")
            forces_report: ForcesReport = format_forces_report(
                config,
                report,
            )
            await log("info", f"{tasks['formatting']}{footer}")
            rich_log(forces_report.findings_report)
            rich_log(forces_report.summary_report)
        else:
            await log(
                "info",
                (
                    "[green]Congratulations! The Agent didn't find "
                    "vulnerable locations that aren't compliant with your "
                    "policies[/]"
                ),
            )

        if config.output:
            temp_file.seek(os.SEEK_SET)
            text_without_ansi_color = remove_color_codes(temp_file.read())
            await in_thread(config.output.write, text_without_ansi_color)
        exit_code = await set_forces_exit_code(config, report.findings)
        await upload_report(
            config=config,
            execution_id=str(uuid.uuid4()).replace("-", ""),
            exit_code=str(exit_code),
            report=report,
            log_file=temp_file.name,
            git_metadata=metadata,
        )
        await log("info", f"{tasks['uploading']}{footer}")
        await log(
            "info", f"Success execution: {exit_code == StatusCode.SUCCESS}"
        )
    return exit_code
