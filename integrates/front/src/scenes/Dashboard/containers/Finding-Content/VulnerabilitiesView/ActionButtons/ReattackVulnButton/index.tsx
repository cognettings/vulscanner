import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";

interface IReattackVulnButtonProps {
  areVulnsSelected: boolean;
  isClosing: boolean;
  isEditing: boolean;
  isFindingReleased: boolean;
  isResubmitting: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  status: "SAFE" | "VULNERABLE";
  onRequestReattack: () => void;
  openModal: () => void;
}

const ReattackVulnButton: React.FC<IReattackVulnButtonProps> = ({
  areVulnsSelected,
  isClosing,
  isEditing,
  isFindingReleased,
  isRequestingReattack,
  isResubmitting,
  isVerifying,
  status,
  onRequestReattack,
  openModal,
}: IReattackVulnButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const shouldRenderRequestVerifyBtn: boolean =
    isFindingReleased &&
    status === "VULNERABLE" &&
    !(isEditing || isVerifying || isResubmitting || isClosing);

  const tooltipMessage = useMemo((): string => {
    if (isRequestingReattack) {
      return t("searchFindings.tabVuln.buttonsTooltip.cancel");
    }

    return t("searchFindings.tabDescription.requestVerify.tooltip");
  }, [isRequestingReattack, t]);

  return (
    <Can do={"api_mutations_request_vulnerabilities_verification_mutate"}>
      {isRequestingReattack ? (
        <Container pr={"8px"}>
          <Button
            disabled={!areVulnsSelected}
            id={"confirm-reattack"}
            onClick={openModal}
            variant={"ghost"}
          >
            <FontAwesomeIcon icon={faCheck} />
            &nbsp;
            {t("searchFindings.tabVuln.buttons.reattack")}
          </Button>
        </Container>
      ) : undefined}
      {shouldRenderRequestVerifyBtn ? (
        <Container pr={"8px"}>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabVuln.buttonsTooltip.cancelReattack.id"}
            tip={tooltipMessage}
          >
            <Button
              id={"start-reattack"}
              onClick={onRequestReattack}
              variant={"ghost"}
            >
              {isRequestingReattack ? (
                <React.Fragment>
                  <FontAwesomeIcon icon={faTimes} />
                  &nbsp;
                  {t("searchFindings.tabDescription.cancelVerify")}
                </React.Fragment>
              ) : (
                <React.Fragment>
                  <FontAwesomeIcon icon={faCheck} />
                  &nbsp;
                  {t("searchFindings.tabDescription.requestVerify.text")}
                </React.Fragment>
              )}
            </Button>
          </Tooltip>
        </Container>
      ) : undefined}
    </Can>
  );
};

export type { IReattackVulnButtonProps };
export { ReattackVulnButton };
