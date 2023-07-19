import _ from "lodash";

import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { getLastTreatment } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import type { IVulnDataAttr } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";

const getVulnsPendingOfAcceptance: (
  vulnerabilities: IVulnRowAttr[]
) => IVulnDataAttr[] = (vulnerabilities: IVulnRowAttr[]): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (pendingVulns: IVulnDataAttr[], vuln: IVulnRowAttr): IVulnDataAttr[] => {
      const lastTreatment: IHistoricTreatment = getLastTreatment(
        vuln.historicTreatment
      );

      return lastTreatment.treatment === "ACCEPTED_UNDEFINED" &&
        lastTreatment.acceptanceStatus === "SUBMITTED"
        ? [...pendingVulns, { acceptance: "APPROVED", ...vuln }]
        : pendingVulns;
    },
    []
  );

const getRequestedZeroRiskVulns: (
  vulnerabilities: IVulnRowAttr[]
) => IVulnDataAttr[] = (vulnerabilities: IVulnRowAttr[]): IVulnDataAttr[] =>
  vulnerabilities.reduce(
    (
      requestedZeroRiskVulns: IVulnDataAttr[],
      vuln: IVulnRowAttr
    ): IVulnDataAttr[] => {
      return vuln.zeroRisk === "Requested"
        ? [...requestedZeroRiskVulns, { acceptance: "", ...vuln }]
        : requestedZeroRiskVulns;
    },
    []
  );

const getRejectedVulns: (vulnerabilities: IVulnRowAttr[]) => IVulnRowAttr[] = (
  vulnerabilities: IVulnRowAttr[]
): IVulnRowAttr[] =>
  vulnerabilities.reduce(
    (submittedVulns: IVulnRowAttr[], vuln: IVulnRowAttr): IVulnRowAttr[] => {
      return vuln.state === "REJECTED"
        ? [...submittedVulns, vuln]
        : submittedVulns;
    },
    []
  );

const getVunerableLocations = (
  vulnerabilities: IVulnRowAttr[]
): IVulnRowAttr[] =>
  vulnerabilities.reduce(
    (vulnerable: IVulnRowAttr[], vuln: IVulnRowAttr): IVulnRowAttr[] => {
      return vuln.state === "VULNERABLE" ? [...vulnerable, vuln] : vulnerable;
    },
    []
  );

const getSubmittedVulns: (vulnerabilities: IVulnRowAttr[]) => IVulnRowAttr[] = (
  vulnerabilities: IVulnRowAttr[]
): IVulnRowAttr[] =>
  vulnerabilities.reduce(
    (submittedVulns: IVulnRowAttr[], vuln: IVulnRowAttr): IVulnRowAttr[] => {
      return vuln.state === "SUBMITTED"
        ? [...submittedVulns, { acceptance: "", ...vuln }]
        : submittedVulns;
    },
    []
  );

function isPendingToAcceptance(vulnerabilities: IVulnRowAttr[]): boolean {
  return (
    getVulnsPendingOfAcceptance(vulnerabilities).length > 0 ||
    getRequestedZeroRiskVulns(vulnerabilities).length > 0 ||
    getSubmittedVulns(vulnerabilities).length > 0
  );
}

const filterVerification = (
  row: IVulnRowAttr,
  value: string | undefined
): boolean => {
  if (value === "" || value === undefined) return true;

  const currentVerification = String(row.verification);
  if (value === "NotRequested") {
    return (
      row.state === "VULNERABLE" &&
      !_.includes(["On_hold", "Requested"], currentVerification)
    );
  }

  return currentVerification.toLowerCase().includes(value.toLowerCase());
};

export {
  getVunerableLocations,
  getVulnsPendingOfAcceptance,
  getRequestedZeroRiskVulns,
  getRejectedVulns,
  getSubmittedVulns,
  isPendingToAcceptance,
  filterVerification,
};
