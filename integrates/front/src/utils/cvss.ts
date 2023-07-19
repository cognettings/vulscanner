/* eslint-disable sort-keys -- Key order for metric values is altered for correct tooltip rendering*/
import _ from "lodash";

import { formatPercentage } from "./formatHelpers";

interface ICVSS3BaseMetrics {
  attackComplexity: string;
  attackVector: string;
  availabilityImpact: string;
  confidentialityImpact: string;
  integrityImpact: string;
  privilegesRequired: string;
  severityScope: string;
  userInteraction: string;
}

interface ICVSS3TemporalMetrics extends ICVSS3BaseMetrics {
  exploitability: string;
  remediationLevel: string;
  reportConfidence: string;
}

interface ICVSS3EnvironmentalMetrics extends ICVSS3TemporalMetrics {
  availabilityRequirement: string;
  confidentialityRequirement: string;
  integrityRequirement: string;
  modifiedAttackComplexity: string;
  modifiedAttackVector: string;
  modifiedAvailabilityImpact: string;
  modifiedConfidentialityImpact: string;
  modifiedIntegrityImpact: string;
  modifiedPrivilegesRequired: string;
  modifiedSeverityScope: string;
  modifiedUserInteraction: string;
}

/**
 * CVSS 3.1 base score metrics.
 * Values were taken from:
 * @see https://www.first.org/cvss/specification-document#7-4-Metric-Values
 */

const attackVectorValues: Record<string, string> = {
  N: "searchFindings.tabSeverity.attackVector.options.network.label",
  A: "searchFindings.tabSeverity.attackVector.options.adjacent.label",
  L: "searchFindings.tabSeverity.attackVector.options.local.label",
  P: "searchFindings.tabSeverity.attackVector.options.physical.label",
};

const attackComplexityValues: Record<string, string> = {
  L: "searchFindings.tabSeverity.attackComplexity.options.low.label",
  H: "searchFindings.tabSeverity.attackComplexity.options.high.label",
};

const privilegesRequiredValues: Record<string, string> = {
  N: "searchFindings.tabSeverity.privilegesRequired.options.none.label",
  L: "searchFindings.tabSeverity.privilegesRequired.options.low.label",
  H: "searchFindings.tabSeverity.privilegesRequired.options.high.label",
};

const userInteractionValues: Record<string, string> = {
  N: "searchFindings.tabSeverity.userInteraction.options.none.label",
  R: "searchFindings.tabSeverity.userInteraction.options.required.label",
};

const severityScopeValues: Record<string, string> = {
  C: "searchFindings.tabSeverity.severityScope.options.changed.label",
  U: "searchFindings.tabSeverity.severityScope.options.unchanged.label",
};

const confidentialityImpactValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.confidentialityImpact.options.high.label",
  L: "searchFindings.tabSeverity.confidentialityImpact.options.low.label",
  N: "searchFindings.tabSeverity.confidentialityImpact.options.none.label",
};

const integrityImpactValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.integrityImpact.options.high.label",
  L: "searchFindings.tabSeverity.integrityImpact.options.low.label",
  N: "searchFindings.tabSeverity.integrityImpact.options.none.label",
};

const availabilityImpactValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.availabilityImpact.options.high.label",
  L: "searchFindings.tabSeverity.availabilityImpact.options.low.label",
  N: "searchFindings.tabSeverity.availabilityImpact.options.none.label",
};

/**
 * CVSS 3.1 temporal score metrics.
 */

const exploitabilityValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.exploitability.options.high.label",
  F: "searchFindings.tabSeverity.exploitability.options.functional.label",
  P: "searchFindings.tabSeverity.exploitability.options.proofOfConcept.label",
  U: "searchFindings.tabSeverity.exploitability.options.unproven.label",
  X: "searchFindings.tabSeverity.exploitability.options.notDefined.label",
};

const remediationLevelValues: Record<string, string> = {
  U: "searchFindings.tabSeverity.remediationLevel.options.unavailable.label",
  W: "searchFindings.tabSeverity.remediationLevel.options.workaround.label",
  T: "searchFindings.tabSeverity.remediationLevel.options.temporaryFix.label",
  O: "searchFindings.tabSeverity.remediationLevel.options.officialFix.label",
  X: "searchFindings.tabSeverity.remediationLevel.options.notDefined.label",
};

const reportConfidenceValues: Record<string, string> = {
  C: "searchFindings.tabSeverity.reportConfidence.options.confirmed.label",
  R: "searchFindings.tabSeverity.reportConfidence.options.reasonable.label",
  U: "searchFindings.tabSeverity.reportConfidence.options.unknown.label",
  X: "searchFindings.tabSeverity.reportConfidence.options.notDefined.label",
};

/**
 * CVSS 3.1 environmental score metrics.
 */

const confidentialityRequirementValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.confidentialityRequirement.options.high.label",
  M: "searchFindings.tabSeverity.confidentialityRequirement.options.medium.label",
  L: "searchFindings.tabSeverity.confidentialityRequirement.options.low.label",
  X: "searchFindings.tabSeverity.confidentialityRequirement.options.notDefined.label",
};

const integrityRequirementValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.integrityRequirement.options.high.label",
  M: "searchFindings.tabSeverity.integrityRequirement.options.medium.label",
  L: "searchFindings.tabSeverity.integrityRequirement.options.low.label",
  X: "searchFindings.tabSeverity.integrityRequirement.options.notDefined.label",
};

const availabilityRequirementValues: Record<string, string> = {
  H: "searchFindings.tabSeverity.availabilityRequirement.options.high.label",
  M: "searchFindings.tabSeverity.availabilityRequirement.options.medium.label",
  L: "searchFindings.tabSeverity.availabilityRequirement.options.low.label",
  X: "searchFindings.tabSeverity.availabilityRequirement.options.notDefined.label",
};

const getCVSS31Values = (vector: string): ICVSS3EnvironmentalMetrics => {
  const notDefined = `X`;
  const metrics = _.reduce(
    vector.split("/"),
    (previous, item): Record<string, string> => ({
      ...previous,
      [item.split(":")[0]]: item.split(":")[1],
    }),
    {}
  );
  const baseMetrics: ICVSS3BaseMetrics = {
    attackComplexity: _.get(metrics, ["AC"]),
    attackVector: _.get(metrics, ["AV"]),
    availabilityImpact: _.get(metrics, ["A"]),
    confidentialityImpact: _.get(metrics, ["C"]),
    integrityImpact: _.get(metrics, ["I"]),
    privilegesRequired: _.get(metrics, ["PR"]),
    severityScope: _.get(metrics, ["S"]),
    userInteraction: _.get(metrics, ["UI"]),
  };
  const temporalMetrics: ICVSS3TemporalMetrics = {
    ...baseMetrics,
    exploitability: _.get(metrics, ["E"], notDefined),
    remediationLevel: _.get(metrics, ["RL"], notDefined),
    reportConfidence: _.get(metrics, ["RC"], notDefined),
  };
  const environmentalMetrics: ICVSS3EnvironmentalMetrics = {
    ...temporalMetrics,
    availabilityRequirement: _.get(metrics, ["AR"], notDefined),
    confidentialityRequirement: _.get(metrics, ["CR"], notDefined),
    integrityRequirement: _.get(metrics, ["IR"], notDefined),
    modifiedAttackComplexity: _.get(metrics, ["MAC"], notDefined),
    modifiedAttackVector: _.get(metrics, ["MAV"], notDefined),
    modifiedAvailabilityImpact: _.get(metrics, ["MA"], notDefined),
    modifiedConfidentialityImpact: _.get(metrics, ["MC"], notDefined),
    modifiedIntegrityImpact: _.get(metrics, ["MI"], notDefined),
    modifiedPrivilegesRequired: _.get(metrics, ["MPR"], notDefined),
    modifiedSeverityScope: _.get(metrics, ["MS"], notDefined),
    modifiedUserInteraction: _.get(metrics, ["MUI"], notDefined),
  };

  return environmentalMetrics;
};

const getCVSS31VectorString = (values: ICVSS3EnvironmentalMetrics): string => {
  const cvssVersion = `CVSS:3.1`;
  const notDefined = `X`;

  return (
    // Base score metrics: mandatory
    `${cvssVersion}/AV:${values.attackVector}` +
    `/AC:${values.attackComplexity}` +
    `/PR:${values.privilegesRequired}` +
    `/UI:${values.userInteraction}` +
    `/S:${values.severityScope}` +
    `/C:${values.confidentialityImpact}` +
    `/I:${values.integrityImpact}` +
    `/A:${values.availabilityImpact}` +
    // Temporal score metrics: optional
    `/E:${values.exploitability || notDefined}` +
    `/RL:${values.remediationLevel || notDefined}` +
    `/RC:${values.reportConfidence || notDefined}` +
    // Environmental score metrics: optional
    `/CR:${values.confidentialityRequirement || notDefined}` +
    `/IR:${values.integrityRequirement || notDefined}` +
    `/AR:${values.availabilityRequirement || notDefined}` +
    `/MAV:${values.modifiedAttackVector || notDefined}` +
    `/MAC:${values.modifiedAttackComplexity || notDefined}` +
    `/MPR:${values.modifiedPrivilegesRequired || notDefined}` +
    `/MUI:${values.modifiedUserInteraction || notDefined}` +
    `/MS:${values.modifiedSeverityScope || notDefined}` +
    `/MC:${values.modifiedConfidentialityImpact || notDefined}` +
    `/MI:${values.modifiedIntegrityImpact || notDefined}` +
    `/MA:${values.modifiedAvailabilityImpact || notDefined}`
  );
};

const getCVSSF = (severity: number): number => {
  return 4 ** (severity - 4);
};

const getRiskExposure = (
  partialCVSSF: number,
  totalCVSSF: number,
  status: string
): string => {
  return formatPercentage(
    totalCVSSF && status === "VULNERABLE" ? partialCVSSF / totalCVSSF : 0,
    true
  );
};

export {
  attackComplexityValues,
  attackVectorValues,
  availabilityImpactValues,
  availabilityRequirementValues,
  confidentialityImpactValues,
  confidentialityRequirementValues,
  exploitabilityValues,
  getCVSS31Values,
  getCVSS31VectorString,
  getCVSSF,
  getRiskExposure,
  integrityImpactValues,
  integrityRequirementValues,
  privilegesRequiredValues,
  remediationLevelValues,
  reportConfidenceValues,
  severityScopeValues,
  userInteractionValues,
};

export type {
  ICVSS3BaseMetrics,
  ICVSS3EnvironmentalMetrics,
  ICVSS3TemporalMetrics,
};
