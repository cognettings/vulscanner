import React from "react";

import { ConfirmVulnerabilityCheckBox } from "./ConfirmVulnerabilityCheckBox";

import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";

export const changeSubmittedFormatter = (
  row: IVulnRowAttr,
  approveFunction: (arg1?: IVulnRowAttr | undefined) => void,
  deleteFunction: (arg1?: IVulnRowAttr | undefined) => void
): JSX.Element => {
  return (
    <ConfirmVulnerabilityCheckBox
      approveFunction={approveFunction}
      deleteFunction={deleteFunction}
      vulnerabilityRow={row}
    />
  );
};
