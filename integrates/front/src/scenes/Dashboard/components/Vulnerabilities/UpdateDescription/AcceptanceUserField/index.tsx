import React from "react";
import { useTranslation } from "react-i18next";

import { Label } from "components/Input";
import type { IAcceptanceUserFieldProps } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/AcceptanceUserField/types";

const AcceptanceUserField: React.FC<IAcceptanceUserFieldProps> = ({
  isAcceptedSelected,
  isAcceptedUndefinedSelected,
  isInProgressSelected,
  lastTreatment,
}: IAcceptanceUserFieldProps): JSX.Element => {
  const { t } = useTranslation();

  const isLastTreatmentAcceptanceStatusApproved: boolean =
    lastTreatment.acceptanceStatus === "APPROVED";

  return (
    <React.StrictMode>
      {(isAcceptedSelected ||
        isAcceptedUndefinedSelected ||
        isInProgressSelected) &&
      isLastTreatmentAcceptanceStatusApproved ? (
        <div className={"mb3 nt2 w-100"}>
          <Label>{t("searchFindings.tabDescription.acceptanceUser")}</Label>
          <p className={"f5 w-fit-content ws-pre-wrap ma0"}>
            {lastTreatment.user}
          </p>
        </div>
      ) : undefined}
    </React.StrictMode>
  );
};

export { AcceptanceUserField };
