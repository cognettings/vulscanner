import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";

interface IResubmitVulnerabilitiesButtonProps {
  areRejectedVulns: boolean;
  isClosing: boolean;
  isEditing: boolean;
  isRequestingReattack: boolean;
  isResubmitting: boolean;
  isVerifying: boolean;
  onCancel?: () => void;
  onResubmit?: () => void;
}

export const ResubmitVulnerabilitiesButton: React.FC<IResubmitVulnerabilitiesButtonProps> =
  ({
    areRejectedVulns,
    isClosing,
    isEditing,
    isRequestingReattack,
    isResubmitting,
    isVerifying,
    onCancel,
    onResubmit,
  }: Readonly<IResubmitVulnerabilitiesButtonProps>): JSX.Element => {
    const { t } = useTranslation();

    const shouldRenderBtn: boolean =
      areRejectedVulns &&
      !(isEditing || isRequestingReattack || isVerifying || isClosing);

    return (
      <Can do={"api_mutations_resubmit_vulnerabilities_mutate"}>
        {shouldRenderBtn ? (
          <Fragment>
            <Container pr={"8px"}>
              <Tooltip
                disp={"inline-block"}
                id={"searchFindings.tabVuln.buttonsTooltip.resubmit.id"}
                place={"bottom"}
                tip={t("searchFindings.tabVuln.buttonsTooltip.resubmit")}
              >
                <Button onClick={onResubmit} variant={"ghost"}>
                  <Fragment>
                    <FontAwesomeIcon icon={faCheck} />
                    &nbsp;{t("searchFindings.tabVuln.buttons.resubmit")}
                  </Fragment>
                </Button>
              </Tooltip>
            </Container>
            {isResubmitting ? (
              <Container pr={"8px"}>
                <Tooltip
                  disp={"inline-block"}
                  id={"searchFindings.tabVuln.buttonsTooltip.cancel.id"}
                  place={"left"}
                  tip={t("searchFindings.tabVuln.buttonsTooltip.cancel")}
                >
                  <Button onClick={onCancel} variant={"ghost"}>
                    <Fragment>
                      <FontAwesomeIcon icon={faTimes} />
                      &nbsp;{t("searchFindings.tabVuln.buttons.cancel")}
                    </Fragment>
                  </Button>
                </Tooltip>
              </Container>
            ) : undefined}
          </Fragment>
        ) : undefined}
      </Can>
    );
  };
