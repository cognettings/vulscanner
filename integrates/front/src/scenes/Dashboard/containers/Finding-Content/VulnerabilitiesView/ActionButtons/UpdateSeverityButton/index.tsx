import { faRuler } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { Can } from "context/authz/Can";

interface IUpdateSeverityButtonProps {
  isDisabled: boolean;
  onUpdateSeverity: () => void;
}

const UpdateSeverityButton: React.FC<IUpdateSeverityButtonProps> = ({
  isDisabled,
  onUpdateSeverity,
}: IUpdateSeverityButtonProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Can do={"api_mutations_update_vulnerabilities_severity_mutate"}>
        <Container>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabDescription.updateSeverity.tooltip.id"}
            tip={t("searchFindings.tabDescription.updateVulnSeverityTooltip")}
          >
            <Button
              disabled={isDisabled}
              id={"vulnerabilities-update-severity"}
              onClick={onUpdateSeverity}
              variant={"ghost"}
            >
              <React.Fragment>
                <FontAwesomeIcon icon={faRuler} />
                &nbsp;
                {t("searchFindings.tabDescription.updateVulnSeverityButton")}
              </React.Fragment>
            </Button>
          </Tooltip>
        </Container>
      </Can>
    </React.StrictMode>
  );
};

export { UpdateSeverityButton };
