import type { ExecutionResult } from "graphql";
import _ from "lodash";

import type {
  IFindingAttr,
  IFindingSuggestionData,
  ITreatmentSummaryAttr,
  IVerificationSummaryAttr,
  IVulnerabilitiesResume,
} from "./types";

import {
  getVulnerabilitiesCriteriaData,
  validateNotEmpty,
} from "../../Finding-Content/DescriptionView/utils";
import type { IRemoveFindingResultAttr } from "../../Finding-Content/types";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

type RemoveFindingResult = ExecutionResult<IRemoveFindingResultAttr>;

const formatReattack: (
  verificationSummary: IVerificationSummaryAttr
) => string = (verificationSummary: IVerificationSummaryAttr): string =>
  translate.t(
    verificationSummary.requested > 0 || verificationSummary.onHold > 0
      ? "group.findings.reattackValues.True"
      : "group.findings.reattackValues.False"
  );

const formatState: (state: string) => JSX.Element = (
  state: string
): JSX.Element => {
  const stateParameters: Record<string, string> = {
    DRAFT: "searchFindings.header.status.stateLabel.draft",
    REJECTED: "searchFindings.header.status.stateLabel.rejected",
    SAFE: "searchFindings.header.status.stateLabel.closed",
    SUBMITTED: "searchFindings.header.status.stateLabel.submitted",
    VULNERABLE: "searchFindings.header.status.stateLabel.open",
    closed: "searchFindings.header.status.stateLabel.closed",
    open: "searchFindings.header.status.stateLabel.open",
  };

  return statusFormatter(translate.t(stateParameters[state]));
};

const formatStatus: (status: string) => JSX.Element = (
  status: string
): JSX.Element => {
  return statusFormatter(status, true);
};

const formatTreatmentSummary: (
  state: "DRAFT" | "SAFE" | "VULNERABLE",
  treatmentSummary: ITreatmentSummaryAttr
) => string = (
  state: "DRAFT" | "SAFE" | "VULNERABLE",
  treatmentSummary: ITreatmentSummaryAttr
): string =>
  state === "VULNERABLE"
    ? `
${translate.t("searchFindings.tabDescription.treatment.new")}: ${
        treatmentSummary.untreated
      },
${translate.t("searchFindings.tabDescription.treatment.inProgress")}: ${
        treatmentSummary.inProgress
      },
${translate.t("searchFindings.tabDescription.treatment.accepted")}: ${
        treatmentSummary.accepted
      },
${translate.t("searchFindings.tabDescription.treatment.acceptedUndefined")}: ${
        treatmentSummary.acceptedUndefined
      }
`
    : "-";

const formatClosingPercentage = (finding: IFindingAttr): number => {
  const { closedVulnerabilities, openVulnerabilities }: IFindingAttr = finding;

  if (openVulnerabilities + closedVulnerabilities === 0) {
    return finding.status === "SAFE" ? 1.0 : 0;
  }

  return closedVulnerabilities / (openVulnerabilities + closedVulnerabilities);
};

const formatFindings = (
  findings: IFindingAttr[],
  findingLocations: Record<string, IVulnerabilitiesResume>
): IFindingAttr[] =>
  findings.map(
    (finding): IFindingAttr => ({
      ...finding,
      closingPercentage: formatClosingPercentage(finding),
      locationsInfo: {
        closedVulnerabilities: finding.closedVulnerabilities,
        findingId: finding.id,
        locations: _.get(findingLocations, finding.id, undefined)?.wheres,
        openVulnerabilities: finding.openVulnerabilities,
        treatmentAssignmentEmails:
          _.get(findingLocations, finding.id, undefined)
            ?.treatmentAssignmentEmails ?? new Set([]),
      },
      reattack: formatReattack(finding.verificationSummary),
      treatment: formatTreatmentSummary(
        finding.status,
        finding.treatmentSummary
      ),
    })
  );

const getAreAllMutationValid = (
  results: ExecutionResult<IRemoveFindingResultAttr>[]
): boolean[] => {
  return results.map(
    (result: ExecutionResult<IRemoveFindingResultAttr>): boolean => {
      if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
        const removeInfoSuccess: boolean = _.isUndefined(
          result.data.removeFinding
        )
          ? true
          : result.data.removeFinding.success;

        return removeInfoSuccess;
      }

      return false;
    }
  );
};

const getResults = async (
  removeFinding: (
    variables: Record<string, unknown>
  ) => Promise<RemoveFindingResult>,
  findings: IFindingAttr[],
  justification: unknown
): Promise<RemoveFindingResult[]> => {
  const chunkSize = 10;
  const vulnChunks = _.chunk(findings, chunkSize);
  const updateChunks = vulnChunks.map(
    (chunk): (() => Promise<RemoveFindingResult[]>) =>
      async (): Promise<RemoveFindingResult[]> => {
        const updates = chunk.map(
          async (finding): Promise<RemoveFindingResult> =>
            removeFinding({
              variables: { findingId: finding.id, justification },
            })
        );

        return Promise.all(updates);
      }
  );

  // Sequentially execute chunks
  return updateChunks.reduce(
    async (previousValue, currentValue): Promise<RemoveFindingResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<RemoveFindingResult[]>([])
  );
};

const handleRemoveFindingsError = (updateError: unknown): void => {
  if (
    _.includes(
      String(updateError),
      translate.t("searchFindings.tabVuln.exceptions.sameValues")
    )
  ) {
    msgError(translate.t("searchFindings.tabVuln.exceptions.sameValues"));
  } else {
    msgError(translate.t("groupAlerts.errorTextsad"));
    Logger.warning("An error occurred removing findings", updateError);
  }
};

async function getFindingSuggestions(
  language: "en" | "es" | undefined = "en"
): Promise<IFindingSuggestionData[]> {
  const vulnsData = await getVulnerabilitiesCriteriaData();

  return Object.keys(vulnsData).map((key: string): IFindingSuggestionData => {
    // Base score metrics
    const attackVector = validateNotEmpty(
      vulnsData[key].score.base.attack_vector
    );
    const attackComplexity = validateNotEmpty(
      vulnsData[key].score.base.attack_complexity
    );
    const privilegesRequired = validateNotEmpty(
      vulnsData[key].score.base.privileges_required
    );
    const userInteraction = validateNotEmpty(
      vulnsData[key].score.base.user_interaction
    );
    const severityScope = validateNotEmpty(vulnsData[key].score.base.scope);
    const confidentialityImpact = validateNotEmpty(
      vulnsData[key].score.base.confidentiality
    );
    const integrityImpact = validateNotEmpty(
      vulnsData[key].score.base.integrity
    );
    const availabilityImpact = validateNotEmpty(
      vulnsData[key].score.base.availability
    );
    // Temporal score metrics
    const exploitability = validateNotEmpty(
      vulnsData[key].score.temporal.exploit_code_maturity
    );

    const remediationLevel = validateNotEmpty(
      vulnsData[key].score.temporal.remediation_level
    );
    const reportConfidence = validateNotEmpty(
      vulnsData[key].score.temporal.report_confidence
    );

    const minTimeToRemediateRaw = validateNotEmpty(
      vulnsData[key].remediation_time
    );
    const minTimeToRemediate = minTimeToRemediateRaw
      ? _.parseInt(minTimeToRemediateRaw)
      : null;
    const { requirements } = vulnsData[key];

    return {
      attackComplexity,
      attackVector,
      attackVectorDescription: validateNotEmpty(
        vulnsData[key][language].impact
      ),
      availabilityImpact,
      code: key,
      confidentialityImpact,
      description: validateNotEmpty(vulnsData[key][language].description),
      exploitability,
      integrityImpact,
      minTimeToRemediate,
      privilegesRequired,
      recommendation: validateNotEmpty(vulnsData[key][language].recommendation),
      remediationLevel,
      reportConfidence,
      severityScope,
      threat: validateNotEmpty(vulnsData[key][language].threat),
      title: validateNotEmpty(vulnsData[key][language].title),
      unfulfilledRequirements: requirements,
      userInteraction,
    };
  });
}

export {
  formatFindings,
  formatState,
  formatStatus,
  formatTreatmentSummary,
  formatReattack,
  getAreAllMutationValid,
  getFindingSuggestions,
  getResults,
  getVulnerabilitiesCriteriaData,
  handleRemoveFindingsError,
};
