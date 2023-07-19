import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";

interface IVerifyVulnerabilitiesButtonProps {
  areVulnsSelected: boolean;
  isClosing: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isResubmitting: boolean;
  isVerified: boolean;
  isVerifying: boolean;
  onVerify: () => void;
  openModal: () => void;
}

export const VerifyVulnerabilitiesButton: React.FC<IVerifyVulnerabilitiesButtonProps> =
  ({
    areVulnsSelected,
    isClosing,
    isEditing,
    isRequestingReattack,
    isResubmitting,
    isVerified,
    isVerifying,
    onVerify,
    openModal,
  }: IVerifyVulnerabilitiesButtonProps): JSX.Element => {
    const { t } = useTranslation();

    const shouldRenderVerifyBtn: boolean =
      !isVerified &&
      !(isEditing || isRequestingReattack || isResubmitting || isClosing);

    const tooltipMessage = useMemo((): string => {
      if (isVerifying) {
        return t("searchFindings.tabVuln.buttonsTooltip.cancel");
      }

      return t("searchFindings.tabDescription.markVerified.tooltip");
    }, [isVerifying, t]);

    const DisplayIcon = useCallback((): JSX.Element => {
      if (isVerifying) {
        return (
          <React.Fragment>
            <FontAwesomeIcon icon={faTimes} />
            &nbsp;{t("searchFindings.tabDescription.cancelVerified")}
          </React.Fragment>
        );
      }

      return (
        <React.Fragment>
          <FontAwesomeIcon icon={faCheck} />
          &nbsp;{t("searchFindings.tabDescription.markVerified.text")}
        </React.Fragment>
      );
    }, [isVerifying, t]);

    return (
      <Can do={"api_mutations_verify_vulnerabilities_request_mutate"}>
        {isVerifying ? (
          <Container pr={"8px"}>
            <Button
              disabled={!areVulnsSelected}
              onClick={openModal}
              variant={"ghost"}
            >
              <FontAwesomeIcon icon={faCheck} />
              &nbsp;{t("searchFindings.tabDescription.markVerified.text")}
            </Button>
          </Container>
        ) : undefined}
        {shouldRenderVerifyBtn ? (
          <Container pr={"8px"}>
            <Tooltip
              disp={"inline-block"}
              id={"searchFindings.tabVuln.buttonsTooltip.cancelVerify.id"}
              place={"top"}
              tip={tooltipMessage}
            >
              <Button onClick={onVerify} variant={"ghost"}>
                <DisplayIcon />
              </Button>
            </Tooltip>
          </Container>
        ) : undefined}
      </Can>
    );
  };
