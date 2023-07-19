from contextlib import (
    suppress,
)
from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
    InvalidParameter,
    InvalidVulnerabilityAlreadyExists,
)
from custom_utils import (
    datetime as datetime_utils,
)
from custom_utils.vulnerabilities import (
    validate_vulnerability_in_toe,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateReason,
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
    VulnerabilityState,
)
from db_model.vulnerabilities.update import (
    update_metadata,
)
import logging
from settings.logger import (
    LOGGING,
)
from vulnerabilities.domain.core import (
    get_vulnerability,
)
from vulnerabilities.domain.utils import (
    get_hash_from_machine_vuln,
)
from vulnerabilities.domain.validations import (
    validate_commit_hash_deco,
    validate_lines_specific_deco,
    validate_uniqueness,
    validate_where_deco,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@validate_commit_hash_deco("vulnerability_commit")
@validate_lines_specific_deco("vulnerability_specific")
@validate_where_deco("vulnerability_where")
async def rebase(
    *,
    loaders: Dataloaders,
    finding_id: str,
    finding_vulns_data: tuple[Vulnerability, ...],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> VulnerabilityState:
    if vulnerability_type != VulnerabilityType.LINES:
        raise ExpectedVulnToBeOfLinesType.new()
    current_vuln: Vulnerability = next(
        vuln for vuln in finding_vulns_data if vuln.id == vulnerability_id
    )
    await validate_vulnerability_in_toe(
        loaders,
        current_vuln._replace(
            state=current_vuln.state._replace(
                specific=vulnerability_specific,
                where=vulnerability_where,
                commit=vulnerability_commit,
            ),
        ),
        index=0,
    )
    current_vuln_hash = hash(current_vuln)
    for vuln in finding_vulns_data:
        if hash(vuln) == current_vuln_hash and vuln.id != current_vuln.id:
            LOGGER.warning(
                "there is a problem with the rebase vulnerability",
                extra={
                    "extra": {
                        "vuln_to_rebase": {
                            "id": current_vuln.id,
                            "path": current_vuln.state.where,
                            "line": current_vuln.state.specific,
                            "root_id": current_vuln.root_id,
                        },
                        "vuln_overwrite": {
                            "id": vuln.id,
                            "path": vuln.state.where,
                            "line": vuln.state.specific,
                            "root_id": vuln.root_id,
                        },
                    }
                },
            )

    try:
        validate_uniqueness(
            finding_vulns_data=finding_vulns_data,
            vulnerability_where=vulnerability_where,
            vulnerability_specific=vulnerability_specific,
            vulnerability_type=vulnerability_type,
            vulnerability_id=vulnerability_id,
        )
    except InvalidVulnerabilityAlreadyExists as exc:
        for vuln in finding_vulns_data:
            if (
                vuln.id == vulnerability_id
                and vuln.state.commit == vulnerability_commit
            ):
                raise exc

    vulns_states = await loaders.vulnerability_historic_state.load(
        vulnerability_id
    )
    last_state = vulns_states[-1]._replace(
        commit=vulnerability_commit,
        specific=vulnerability_specific,
        where=vulnerability_where,
        modified_date=datetime_utils.get_utc_now(),
        modified_by="rebase@fluidattacks.com",
        source=Source.ASM,
    )

    await vulns_model.update_historic_entry(
        current_value=current_vuln,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        entry=last_state,
    )
    with suppress(InvalidParameter):
        loaders.vulnerability.clear(vulnerability_id)
        await update_metadata(
            vulnerability_id=vulnerability_id,
            finding_id=finding_id,
            metadata=VulnerabilityMetadataToUpdate(
                hash=await get_hash_from_machine_vuln(
                    loaders, await get_vulnerability(loaders, vulnerability_id)
                )
            ),
        )
    return last_state


async def close_vulnerability(
    loaders: Dataloaders,
    vulnerability_id: str,
    vulnerability_commit: str,
    vulnerability_where: str,
    vulnerability_specific: str,
) -> None:
    vulnerability = await loaders.vulnerability.load(vulnerability_id)
    if not vulnerability:
        return
    vulns_states = await loaders.vulnerability_historic_state.load(
        vulnerability_id
    )
    last_state = vulns_states[-1]._replace(
        commit=vulnerability_commit,
        specific=vulnerability_specific,
        where=vulnerability_where,
        modified_date=datetime_utils.get_utc_now(),
        modified_by="rebase@fluidattacks.com",
        source=Source.ASM,
        reasons=[VulnerabilityStateReason.CONSISTENCY],
        status=VulnerabilityStateStatus.SAFE,
        other_reason=(
            "The content of the vulnerability "
            "could not be found in the HEAD commit."
        ),
    )

    await vulns_model.update_historic_entry(
        current_value=vulnerability,
        finding_id=vulnerability.finding_id,
        vulnerability_id=vulnerability_id,
        entry=last_state,
    )
    with suppress(InvalidParameter):
        loaders.vulnerability.clear(vulnerability_id)
        await update_metadata(
            vulnerability_id=vulnerability_id,
            finding_id=vulnerability.finding_id,
            metadata=VulnerabilityMetadataToUpdate(
                hash=await get_hash_from_machine_vuln(
                    loaders, await get_vulnerability(loaders, vulnerability_id)
                )
            ),
        )
