import aioboto3
from config import (
    dump_to_yaml,
)
from contextlib import (
    suppress,
)
from core.result import (
    get_sarif,
)
import csv
import ctx
from custom_exceptions import (
    NoOutputFilePathSpecified,
)
import json
from lib.apk.analyze import (
    analyze as analyze_apk,
)
from lib.dast.aws.analyze import (
    analyze as analyze_dast_aws,
)
from lib.http.analyze import (
    analyze as analyze_http,
)
from lib.sast.analyze import (
    analyze as analyze_sast,
)
from lib.sca.analyze import (
    analyze as analyze_sca,
)
from lib.ssl.analyze import (
    analyze as analyze_ssl,
)
from model import (
    core,
)
import os
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
    reset as reset_ephemeral_state,
)
import tempfile
from utils.bugs import (
    add_bugsnag_data,
)
from utils.logs import (
    configure as configure_logs,
    log_blocking,
    log_to_remote_blocking,
)
from utils.repositories import (
    get_repo_head_hash,
)
from zone import (
    t,
)


async def upload_sarif_result(
    stores: dict[core.FindingEnum, EphemeralStore],
) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = f"{tmp_dir}/{ctx.SKIMS_CONFIG.execution_id}.csv"
        notify_findings_as_sarif(stores=stores, output_path=file_path)
        with open(file_path, "rb") as reader:
            session = aioboto3.Session()
            async with session.client("s3") as s3_client:
                await s3_client.upload_fileobj(
                    reader,
                    "machine.data",
                    f"results/{ctx.SKIMS_CONFIG.execution_id}.sarif",
                )


async def execute_skims(
    stores: dict[core.FindingEnum, EphemeralStore] | None = None,
) -> dict[core.FindingEnum, EphemeralStore]:
    """
    Execute skims according to the provided config.

    :raises MemoryError: If not enough memory can be allocated by the runtime
    :raises SystemExit: If any critical error occurs
    """

    stores = stores or {
        finding: get_ephemeral_store() for finding in core.FindingEnum
    }
    if ctx.SKIMS_CONFIG.sca.include:
        analyze_sca(stores=stores)
    if ctx.SKIMS_CONFIG.apk.include:
        analyze_apk(stores=stores)
    if ctx.SKIMS_CONFIG.sast.include:
        analyze_sast(stores=stores)
    if ctx.SKIMS_CONFIG.dast:
        if ctx.SKIMS_CONFIG.dast.ssl_checks:
            await analyze_ssl(stores=stores)
        if ctx.SKIMS_CONFIG.dast.http_checks:
            await analyze_http(stores=stores)
        for aws_cred in ctx.SKIMS_CONFIG.dast.aws_credentials:
            if aws_cred:
                await analyze_dast_aws(credentials=aws_cred, stores=stores)

    report_results(stores=stores)
    return stores


def report_results(
    stores: dict[core.FindingEnum, EphemeralStore],
) -> None:
    if ctx.SKIMS_CONFIG.output:
        if ctx.SKIMS_CONFIG.output.format == core.OutputFormat.CSV:
            notify_findings_as_csv(
                stores=stores, output=ctx.SKIMS_CONFIG.output.file_path
            )
        elif ctx.SKIMS_CONFIG.output.format == core.OutputFormat.SARIF:
            notify_findings_as_sarif(stores=stores)
    else:
        notify_findings_as_snippets(stores)


def notify_findings_as_snippets(
    stores: dict[core.FindingEnum, EphemeralStore],
) -> None:
    """Print user-friendly messages about the results found."""
    for store in stores.values():
        for result in store.iterate():
            if result.skims_metadata:
                title = t(result.finding.value.title)
                what = result.what_on_integrates
                kind = result.kind.value
                snippet = result.skims_metadata.snippet
                cwe = " + ".join(
                    map(str, sorted(result.skims_metadata.cwe_ids))
                )
                cvss = result.skims_metadata.cvss
                vuln_url = (
                    "https://docs.fluidattacks.com/criteria/vulnerabilities/"
                    + result.finding.name.replace("F", "")
                )
                log_blocking(
                    "info",
                    f"{title}: {what} found by {kind} module.\n\n{snippet}\n"
                    f"{cwe} - {cvss}\nMore information in: {vuln_url}\n",
                )


def notify_findings_as_csv(
    stores: dict[core.FindingEnum, EphemeralStore],
    output: str,
) -> int:
    headers = (
        "title",
        "cwe",
        "description",
        "cvss",
        "finding",
        "stream",
        "kind",
        "where",
        "snippet",
        "method",
    )

    rows = [
        dict(
            cwe=" + ".join(map(str, sorted(result.skims_metadata.cwe_ids))),
            description=result.skims_metadata.description,
            kind=result.kind.value,
            cvss=result.skims_metadata.cvss,
            method=result.skims_metadata.source_method,
            snippet=f"\n{snippet}\n",
            stream=result.stream,
            title=t(result.finding.value.title),
            where=result.where,
            finding=(
                "https://docs.fluidattacks.com/criteria/vulnerabilities/"
                + result.finding.name.replace("F", "")
            ),
        )
        for store in stores.values()
        for result in store.iterate()
        for snippet in [
            result.skims_metadata.snippet.replace("\x00", "")
            if result.skims_metadata
            else ""
        ]
        if result.skims_metadata
    ]

    summary = (
        f"Summary: {len(rows)} vulnerabilities were found in your targets."
        if len(rows) != 0
        else "Summary: No vulnerabilities were found in your targets."
    )
    with open(output, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in sorted(rows, key=str):
            with suppress(UnicodeEncodeError):
                writer.writerow(row)
        file.write(summary)

    log_blocking("info", "An output file has been written: %s", output)
    return len(rows)


def notify_findings_as_sarif(
    stores: dict[core.FindingEnum, EphemeralStore],
    output_path: str | None = None,
) -> None:
    if output_path is None and ctx.SKIMS_CONFIG.output is None:
        log_to_remote_blocking(
            msg="No output file path specified for SARIF output",
            severity="warning",
            config=dump_to_yaml(config=ctx.SKIMS_CONFIG),
        )
        raise NoOutputFilePathSpecified()

    file_path: str
    if output_path is not None:
        file_path = output_path
    elif ctx.SKIMS_CONFIG.output is not None:
        file_path = ctx.SKIMS_CONFIG.output.file_path

    result = get_sarif(stores)
    with open(file_path, "w", encoding="utf-8") as writer:
        json.dump(result, writer)


async def main() -> tuple[bool, int]:
    try:
        configure_logs()
        add_bugsnag_data(namespace=ctx.SKIMS_CONFIG.namespace)

        reset_ephemeral_state()
        log_blocking(
            "info",
            (
                "Official Documentation:"
                " https://docs.fluidattacks.com/tech/scanner/standalone/"
            ),
        )
        log_blocking("info", f"Namespace: {ctx.SKIMS_CONFIG.namespace}")
        commit = ctx.SKIMS_CONFIG.commit or get_repo_head_hash(
            ctx.SKIMS_CONFIG.working_dir
        )
        log_blocking("info", f"info HEAD is now at: {commit}")
        log_blocking(
            "info", f"Startup work dir is: {ctx.SKIMS_CONFIG.start_dir}"
        )
        log_blocking(
            "info", f"Moving work dir to: {ctx.SKIMS_CONFIG.working_dir}"
        )

        os.chdir(ctx.SKIMS_CONFIG.working_dir)

        stores = await execute_skims()

        total_vulns = 0
        for store in stores.values():
            for _ in store.iterate():
                total_vulns += 1
        success = True

        return success, total_vulns
    finally:
        if ctx.SKIMS_CONFIG.start_dir:
            os.chdir(ctx.SKIMS_CONFIG.start_dir)
            reset_ephemeral_state()
