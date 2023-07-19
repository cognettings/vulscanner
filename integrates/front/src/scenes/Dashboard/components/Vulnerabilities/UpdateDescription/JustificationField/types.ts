import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

interface IJustificationFieldProps {
  areSelectedSubmittedVulnerabilities: boolean;
  isTreatmentPristine: boolean;
  lastTreatment: IHistoricTreatment;
}

export type { IJustificationFieldProps };
