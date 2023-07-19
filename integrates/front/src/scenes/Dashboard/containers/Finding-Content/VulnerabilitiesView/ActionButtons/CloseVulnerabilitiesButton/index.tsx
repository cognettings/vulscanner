import { faCheck, faTimes } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import type { ICloseVulnerabilitiesButtonProps } from "./types";

import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";

export const CloseVulnerabilitiesButton: React.FC<ICloseVulnerabilitiesButtonProps> =
  ({
    areVulnerableLocations,
    isClosing,
    isEditing,
    isRequestingReattack,
    isResubmitting,
    isVerifying,
    onCancel = undefined,
    onClosing = undefined,
  }): JSX.Element => {
    const { t } = useTranslation();

    const shouldRenderBtn =
      areVulnerableLocations &&
      !(isEditing || isRequestingReattack || isVerifying || isResubmitting);

    return (
      <Can do={"api_mutations_close_vulnerabilities_mutate"}>
        {shouldRenderBtn ? (
          <Fragment>
            <Container pr={"8px"}>
              <Tooltip
                disp={"inline-block"}
                id={"searchFindings.tabVuln.buttonsTooltip.close.id"}
                place={"bottom"}
                tip={t("searchFindings.tabVuln.buttonsTooltip.close")}
              >
                <ConfirmDialog
                  message={t("searchFindings.tabVuln.buttons.close.message")}
                  title={t("searchFindings.tabVuln.buttons.close.title")}
                >
                  {(confirm): JSX.Element => {
                    return (
                      <Button onClick={onClosing?.(confirm)} variant={"ghost"}>
                        <Fragment>
                          <FontAwesomeIcon icon={faCheck} />
                          &nbsp;{t("searchFindings.tabVuln.buttons.close.text")}
                        </Fragment>
                      </Button>
                    );
                  }}
                </ConfirmDialog>
              </Tooltip>
            </Container>
            {isClosing ? (
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
