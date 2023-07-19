import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useContext } from "react";
import { useTranslation } from "react-i18next";

import type { IHandleAcceptanceButtonProps } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";

const HandleAcceptanceButton: React.FC<IHandleAcceptanceButtonProps> = ({
  areVulnsPendingOfAcceptance,
  areRequestedZeroRiskVulns,
  areSubmittedVulns,
  isClosing,
  isEditing,
  isRequestingReattack,
  isResubmitting,
  isVerifying,
  openHandleAcceptance,
}: IHandleAcceptanceButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const canHandleVulnsAcceptance: boolean = permissions.can(
    "api_mutations_handle_vulnerabilities_acceptance_mutate"
  );
  const canConfirmZeroRiskVuln: boolean =
    permissions.can("api_mutations_confirm_vulnerabilities_zero_risk_mutate") &&
    attributes.can("can_request_zero_risk");
  const canRejectZeroRiskVuln: boolean =
    permissions.can("api_mutations_reject_vulnerabilities_zero_risk_mutate") &&
    attributes.can("can_request_zero_risk");
  const canConfirmVulnerabilities: boolean = permissions.can(
    "api_mutations_confirm_vulnerabilities_mutate"
  );
  const canRejectVulnerabilities: boolean = permissions.can(
    "api_mutations_reject_vulnerabilities_mutate"
  );
  const canUpdateVulns: boolean = attributes.can("can_report_vulnerabilities");

  const shouldRenderHandleAcceptanceBtn: boolean =
    ((canHandleVulnsAcceptance && areVulnsPendingOfAcceptance) ||
      ((canConfirmZeroRiskVuln || canRejectZeroRiskVuln) &&
        areRequestedZeroRiskVulns) ||
      ((canConfirmVulnerabilities || canRejectVulnerabilities) &&
        canUpdateVulns &&
        areSubmittedVulns)) &&
    !(
      isEditing ||
      isRequestingReattack ||
      isVerifying ||
      isResubmitting ||
      isClosing
    );

  return (
    <React.StrictMode>
      {shouldRenderHandleAcceptanceBtn ? (
        <Container pr={"8px"}>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabVuln.buttonsTooltip.handleAcceptance.id"}
            place={"top"}
            tip={t("searchFindings.tabVuln.buttonsTooltip.handleAcceptance")}
          >
            <Button
              id={"handleAcceptanceButton"}
              onClick={openHandleAcceptance}
              variant={"ghost"}
            >
              <React.Fragment>
                <FontAwesomeIcon icon={faCheck} />
                &nbsp;
                {t("searchFindings.tabVuln.buttons.handleAcceptance")}
              </React.Fragment>
            </Button>
          </Tooltip>
        </Container>
      ) : undefined}
    </React.StrictMode>
  );
};

export { HandleAcceptanceButton };
