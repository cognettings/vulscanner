/* eslint-disable sort-keys -- Key order for metric values is altered for correct tooltip rendering*/
import type { ISeverityField } from "scenes/Dashboard/containers/Finding-Content/SeverityView/types";
import type { ICVSS3EnvironmentalMetrics } from "utils/cvss";
import {
  attackComplexityValues,
  attackVectorValues,
  availabilityImpactValues,
  availabilityRequirementValues,
  confidentialityImpactValues,
  confidentialityRequirementValues,
  exploitabilityValues,
  integrityImpactValues,
  integrityRequirementValues,
  privilegesRequiredValues,
  remediationLevelValues,
  reportConfidenceValues,
  severityScopeValues,
  userInteractionValues,
} from "utils/cvss";
import { translate } from "utils/translations/translate";

const attackVectorBgColors: Record<string, string> = {
  N: "bg-dark-red",
  A: "bg-red",
  L: "bg-orange",
  P: "bg-lbl-yellow",
};

const attackComplexityBgColors: Record<string, string> = {
  L: "bg-dark-red",
  H: "bg-lbl-yellow",
};

const privilegesRequiredBgColors: Record<string, string> = {
  N: "bg-dark-red",
  L: "bg-orange",
  H: "bg-lbl-yellow",
};

const userInteractionBgColors: Record<string, string> = {
  N: "bg-dark-red",
  R: "bg-lbl-yellow",
};

const severityScopeBgColors: Record<string, string> = {
  C: "bg-dark-red",
  U: "bg-lbl-yellow",
};

const confidentialityImpactBgColors: Record<string, string> = {
  H: "bg-dark-red",
  L: "bg-lbl-yellow",
  N: "bg-lbl-green",
};

const integrityImpactBgColors: Record<string, string> = {
  H: "bg-dark-red",
  L: "bg-lbl-yellow",
  N: "bg-lbl-green",
};

const availabilityImpactBgColors: Record<string, string> = {
  H: "bg-dark-red",
  L: "bg-lbl-yellow",
  N: "bg-lbl-green",
};

const exploitabilityBgColors: Record<string, string> = {
  H: "bg-dark-red",
  F: "bg-red",
  P: "bg-orange",
  U: "bg-lbl-yellow",
  X: "bg-gray",
};

const remediationLevelBgColors: Record<string, string> = {
  U: "bg-dark-red",
  W: "bg-orange",
  T: "bg-lbl-yellow",
  O: "bg-lbl-green",
  X: "bg-gray",
};

const reportConfidenceBgColors: Record<string, string> = {
  C: "bg-dark-red",
  R: "bg-orange",
  U: "bg-lbl-yellow",
  X: "bg-gray",
};

const castFieldsCVSS3: (
  dataset: ICVSS3EnvironmentalMetrics
) => ISeverityField[] = (
  dataset: ICVSS3EnvironmentalMetrics
): ISeverityField[] => {
  const fields: ISeverityField[] = [
    {
      currentValue: dataset.attackVector,
      name: "attackVector",
      options: attackVectorValues,
      title: translate.t("searchFindings.tabSeverity.attackVector.label"),
    },
    {
      currentValue: dataset.attackComplexity,
      name: "attackComplexity",
      options: attackComplexityValues,
      title: translate.t("searchFindings.tabSeverity.attackComplexity.label"),
    },
    {
      currentValue: dataset.userInteraction,
      name: "userInteraction",
      options: userInteractionValues,
      title: translate.t("searchFindings.tabSeverity.userInteraction.label"),
    },
    {
      currentValue: dataset.severityScope,
      name: "severityScope",
      options: severityScopeValues,
      title: translate.t("searchFindings.tabSeverity.severityScope.label"),
    },
    {
      currentValue: dataset.confidentialityImpact,
      name: "confidentialityImpact",
      options: confidentialityImpactValues,
      title: translate.t(
        "searchFindings.tabSeverity.confidentialityImpact.label"
      ),
    },
    {
      currentValue: dataset.integrityImpact,
      name: "integrityImpact",
      options: integrityImpactValues,
      title: translate.t("searchFindings.tabSeverity.integrityImpact.label"),
    },
    {
      currentValue: dataset.availabilityImpact,
      name: "availabilityImpact",
      options: availabilityImpactValues,
      title: translate.t("searchFindings.tabSeverity.availabilityImpact.label"),
    },
    {
      currentValue: dataset.exploitability,
      name: "exploitability",
      options: exploitabilityValues,
      title: translate.t("searchFindings.tabSeverity.exploitability.label"),
    },
    {
      currentValue: dataset.remediationLevel,
      name: "remediationLevel",
      options: remediationLevelValues,
      title: translate.t("searchFindings.tabSeverity.remediationLevel.label"),
    },
    {
      currentValue: dataset.reportConfidence,
      name: "reportConfidence",
      options: reportConfidenceValues,
      title: translate.t("searchFindings.tabSeverity.reportConfidence.label"),
    },
    {
      currentValue: dataset.privilegesRequired,
      name: "privilegesRequired",
      options: privilegesRequiredValues,
      title: translate.t("searchFindings.tabSeverity.privilegesRequired.label"),
    },
  ];

  const environmentFields: ISeverityField[] = [
    {
      currentValue: dataset.confidentialityRequirement,
      name: "confidentialityRequirement",
      options: confidentialityRequirementValues,
      title: translate.t(
        "searchFindings.tabSeverity.confidentialityRequirement.label"
      ),
    },
    {
      currentValue: dataset.integrityRequirement,
      name: "integrityRequirement",
      options: integrityRequirementValues,
      title: translate.t(
        "searchFindings.tabSeverity.integrityRequirement.label"
      ),
    },
    {
      currentValue: dataset.availabilityRequirement,
      name: "availabilityRequirement",
      options: availabilityRequirementValues,
      title: translate.t(
        "searchFindings.tabSeverity.availabilityRequirement.label"
      ),
    },
    {
      currentValue: dataset.modifiedAttackVector,
      name: "modifiedAttackVector",
      options: attackVectorValues,
      title: translate.t("searchFindings.tabSeverity.modifiedAttackVector"),
    },
    {
      currentValue: dataset.modifiedAttackComplexity,
      name: "modifiedAttackComplexity",
      options: attackComplexityValues,
      title: translate.t("searchFindings.tabSeverity.modifiedAttackComplexity"),
    },
    {
      currentValue: dataset.modifiedUserInteraction,
      name: "modifiedUserInteraction",
      options: userInteractionValues,
      title: translate.t("searchFindings.tabSeverity.modifiedUserInteraction"),
    },
    {
      currentValue: dataset.modifiedSeverityScope,
      name: "modifiedSeverityScope",
      options: severityScopeValues,
      title: translate.t("searchFindings.tabSeverity.modifiedSeverityScope"),
    },
    {
      currentValue: dataset.modifiedConfidentialityImpact,
      name: "modifiedConfidentialityImpact",
      options: confidentialityImpactValues,
      title: translate.t(
        "searchFindings.tabSeverity.modifiedConfidentialityImpact"
      ),
    },
    {
      currentValue: dataset.modifiedIntegrityImpact,
      name: "modifiedIntegrityImpact",
      options: integrityImpactValues,
      title: translate.t("searchFindings.tabSeverity.modifiedIntegrityImpact"),
    },
    {
      currentValue: dataset.modifiedAvailabilityImpact,
      name: "modifiedAvailabilityImpact",
      options: availabilityImpactValues,
      title: translate.t(
        "searchFindings.tabSeverity.modifiedAvailabilityImpact"
      ),
    },
    {
      currentValue: dataset.modifiedPrivilegesRequired,
      name: "modifiedPrivilegesRequired",
      options: privilegesRequiredValues,
      title: translate.t(
        "searchFindings.tabSeverity.modifiedPrivilegesRequired"
      ),
    },
  ];

  return [...fields, ...environmentFields];
};

export {
  attackComplexityBgColors,
  attackVectorBgColors,
  availabilityImpactBgColors,
  castFieldsCVSS3,
  confidentialityImpactBgColors,
  exploitabilityBgColors,
  integrityImpactBgColors,
  privilegesRequiredBgColors,
  remediationLevelBgColors,
  reportConfidenceBgColors,
  severityScopeBgColors,
  userInteractionBgColors,
};
