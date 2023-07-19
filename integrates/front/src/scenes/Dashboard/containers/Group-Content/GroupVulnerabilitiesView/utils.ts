import _ from "lodash";

import type { IGroupVulnerabilities, IGroupVulnerabilityDrafts } from "./types";

import type { IHistoricTreatment } from "../../Finding-Content/DescriptionView/types";
import type { IVulnerabilitiesAttr } from "../../Finding-Content/VulnerabilitiesView/types";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { formatHistoricTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";

const formatVulnAttribute: (state: string) => string = (
  state: string
): string => {
  const vulnParameters: Record<string, string> = {
    currentState: "stateStatus",
    root: "root",
    treatment: "treatment",
    type: "type",
    verification: "verificationStatus",
  };

  return vulnParameters[state];
};

const formatVulnerability: (data: IGroupVulnerabilities) => IVulnRowAttr[] = (
  data: IGroupVulnerabilities
): IVulnRowAttr[] => {
  const vulnerabilityFormat = data.group.vulnerabilities.edges
    .map((edge): IVulnRowAttr => edge.node)
    .map((vulnerability): IVulnRowAttr => {
      const lastTreatment: IHistoricTreatment =
        formatHistoricTreatment(vulnerability);

      return {
        ...vulnerability,
        historicTreatment: [lastTreatment],
      };
    });

  return vulnerabilityFormat;
};

const formatVulnerabilityDrafts: (
  data: IGroupVulnerabilityDrafts
) => IVulnRowAttr[] = (data: IGroupVulnerabilityDrafts): IVulnRowAttr[] => {
  if (_.isUndefined(data.group.vulnerabilityDrafts)) {
    return [];
  }
  const vulnerabilityFormat = data.group.vulnerabilityDrafts.edges
    .map((edge): IVulnRowAttr => edge.node)
    .map((vulnerability): IVulnRowAttr => {
      const lastTreatment: IHistoricTreatment =
        formatHistoricTreatment(vulnerability);

      return {
        ...vulnerability,
        historicTreatment: [lastTreatment],
      };
    });

  return vulnerabilityFormat;
};

function isPendingToAcceptance(
  vulnerabilitiesZeroRisk: IVulnerabilitiesAttr[]
): boolean {
  return vulnerabilitiesZeroRisk.length > 0;
}

export {
  formatVulnAttribute,
  formatVulnerability,
  formatVulnerabilityDrafts,
  isPendingToAcceptance,
};
