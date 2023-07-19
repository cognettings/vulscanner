from dataloaders import (
    Dataloaders,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decimal import (
    Decimal,
)


async def get_efficacy(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> Decimal:
    if (
        vuln.state.status != VulnerabilityStateStatus.SAFE
        or not vuln.verification
    ):
        return Decimal(0)

    if (
        vuln.unreliable_indicators.unreliable_reattack_cycles
        and vuln.verification.status
        == VulnerabilityVerificationStatus.VERIFIED
    ):
        # If the indicator is present, we'll trust it
        cycles = vuln.unreliable_indicators.unreliable_reattack_cycles
    else:
        cycles = await get_reattack_cycles(loaders, vuln)

    if cycles:
        return Decimal(100 / cycles).quantize(Decimal("0.01"))
    return Decimal(0)


async def get_reattack_cycles(
    loaders: Dataloaders,
    vuln: Vulnerability,
) -> int:
    historic = await loaders.vulnerability_historic_verification.load(vuln.id)

    return len(
        [
            verification
            for verification in historic
            if verification.status == VulnerabilityVerificationStatus.REQUESTED
        ]
    )
