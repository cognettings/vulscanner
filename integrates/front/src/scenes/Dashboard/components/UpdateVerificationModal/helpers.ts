import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";

import type { IVulnData } from ".";
import type {
  IRequestVulnVerificationResult,
  IVerifyRequestVulnResult,
  ReattackVulnerabilitiesResult,
  VerificationResult,
  VerifyVulnerabilitiesResult,
} from "scenes/Dashboard/components/UpdateVerificationModal/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleRequestVerification = (
  clearSelected: () => void,
  setRequestState: () => void,
  data: boolean
): void => {
  if (data) {
    msgSuccess(
      translate.t("groupAlerts.requestedReattackSuccess"),
      translate.t("groupAlerts.updatedTitle")
    );
    setRequestState();
    clearSelected();
  }
};

const handleRequestVerificationError = (error: GraphQLError): void => {
  switch (error.message) {
    case "Exception - Request verification already requested":
      msgError(translate.t("groupAlerts.verificationAlreadyRequested"));
      break;
    case "Exception - The vulnerability has already been closed":
      msgError(translate.t("groupAlerts.vulnClosed"));
      break;
    case "Exception - Vulnerability not found":
      msgError(translate.t("groupAlerts.noFound"));
      break;
    case "Exception - Access denied or credential not found":
      msgError(translate.t("group.scope.git.sync.noCredentials"));
      break;
    case "Exception - The git repository is outdated":
      msgError(translate.t("groupAlerts.outdatedRepository"));
      break;
    case "Exception - Error value is not valid":
      msgError(translate.t("group.scope.git.errors.invalidGitCredentials"));
      break;
    default:
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred requesting verification", error);
  }
};

const handleVerifyRequest = (
  clearSelected: () => void,
  setVerifyState: () => void,
  data: boolean,
  numberOfVulneabilities: number
): void => {
  if (data) {
    msgSuccess(
      translate.t(
        `groupAlerts.verifiedSuccess${
          numberOfVulneabilities > 1 ? "Plural" : ""
        }`
      ),
      translate.t("groupAlerts.updatedTitle")
    );
    setVerifyState();
    clearSelected();
  }
};

const handleVerifyRequestError = (error: GraphQLError): void => {
  switch (error.message) {
    case "Exception - Error verification not requested":
      msgError(translate.t("groupAlerts.noVerificationRequested"));
      break;
    case "Exception - Vulnerability not found":
      msgError(translate.t("groupAlerts.noFound"));
      break;
    case "Exception - The git repository is outdated":
      msgError(translate.t("groupAlerts.outdatedRepository"));
      break;
    default:
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred verifying a request", error);
  }
};

const getAreAllMutationValid = (
  results: ReattackVulnerabilitiesResult[] | VerifyVulnerabilitiesResult[]
): boolean[] => {
  return results.map(
    (
      result: ReattackVulnerabilitiesResult | VerifyVulnerabilitiesResult
    ): boolean => {
      if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
        const reattackSuccess: boolean = _.isUndefined(
          (result.data as IRequestVulnVerificationResult)
            .requestVulnerabilitiesVerification
        )
          ? false
          : (result.data as IRequestVulnVerificationResult)
              .requestVulnerabilitiesVerification.success;

        const verifySuccess: boolean = _.isUndefined(
          (result.data as IVerifyRequestVulnResult).verifyVulnerabilitiesRequest
        )
          ? false
          : (result.data as IVerifyRequestVulnResult)
              .verifyVulnerabilitiesRequest.success;

        return reattackSuccess || verifySuccess;
      }

      return false;
    }
  );
};

const getAreAllChunckedMutationValid = (
  results: VerificationResult[]
): boolean[] =>
  results
    .map(getAreAllMutationValid)
    .reduce(
      (previous: boolean[], current: boolean[]): boolean[] => [
        ...previous,
        ...current,
      ],
      []
    );

const handleSubmitHelper = async (
  requestVerification: (
    variables: Record<string, unknown>
  ) => Promise<ReattackVulnerabilitiesResult>,
  verifyRequest: (
    variables: Record<string, unknown>
  ) => Promise<VerifyVulnerabilitiesResult>,
  findingId: string,
  values: { treatmentJustification: string },
  vulns: IVulnData[],
  vulnerabilitiesList: IVulnData[],
  isReattacking: boolean
): Promise<ReattackVulnerabilitiesResult[] | VerifyVulnerabilitiesResult[]> => {
  const chunkSize = 80;
  if (isReattacking) {
    const vulnerabilitiesId: string[] = vulns.map(
      (vuln: IVulnData): string => vuln.id
    );

    mixpanel.track("RequestReattack");
    const vulnerabilitiesIdsChunks: string[][] = _.chunk(
      vulnerabilitiesId,
      chunkSize
    );
    const requestedChunks = vulnerabilitiesIdsChunks.map(
      (
          chunkedVulnerabilitiesIds
        ): (() => Promise<ReattackVulnerabilitiesResult[]>) =>
        async (): Promise<ReattackVulnerabilitiesResult[]> => {
          return Promise.all([
            requestVerification({
              variables: {
                findingId,
                justification: values.treatmentJustification,
                vulnerabilities: chunkedVulnerabilitiesIds,
              },
            }),
          ]);
        }
    );

    return requestedChunks.reduce(
      async (
        previousValue,
        currentValue
      ): Promise<ReattackVulnerabilitiesResult[]> => [
        ...(await previousValue),
        ...(await currentValue()),
      ],
      Promise.resolve<ReattackVulnerabilitiesResult[]>([])
    );
  }
  const VulnerabilitiesListChunks: IVulnData[][] = _.chunk(
    vulnerabilitiesList,
    chunkSize
  );
  const verifiedChunks = VulnerabilitiesListChunks.map(
    (
        chunkedVulnerabilitiesList
      ): (() => Promise<VerifyVulnerabilitiesResult[]>) =>
      async (): Promise<VerifyVulnerabilitiesResult[]> => {
        const openVulnsId: string[] = chunkedVulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData): string[] =>
            vuln.state === "VULNERABLE" ? [...acc, vuln.id] : acc,
          []
        );
        const closedVulnsId: string[] = chunkedVulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData): string[] =>
            vuln.state === "SAFE" ? [...acc, vuln.id] : acc,
          []
        );

        return Promise.all([
          verifyRequest({
            variables: {
              closedVulns: closedVulnsId,
              findingId,
              justification: values.treatmentJustification,
              openVulns: openVulnsId,
            },
          }),
        ]);
      }
  );

  return verifiedChunks.reduce(
    async (
      previousValue,
      currentValue
    ): Promise<VerifyVulnerabilitiesResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<VerifyVulnerabilitiesResult[]>([])
  );
};

const handleAltSubmitHelper = async (
  requestVerification: (
    variables: Record<string, unknown>
  ) => Promise<ReattackVulnerabilitiesResult>,
  verifyRequest: (
    variables: Record<string, unknown>
  ) => Promise<VerifyVulnerabilitiesResult>,
  values: { treatmentJustification: string },
  vulnerabilitiesList: IVulnData[],
  isReattacking: boolean
): Promise<VerificationResult[]> => {
  const vulnerabilitiesByFinding = _.groupBy(
    vulnerabilitiesList,
    (vuln: IVulnData): string => vuln.findingId
  );
  const requestedChunks = Object.entries(vulnerabilitiesByFinding).map(
    ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnData[]
      ]): (() => Promise<VerificationResult[]>) =>
      async (): Promise<VerificationResult[]> => {
        return Promise.all([
          handleSubmitHelper(
            requestVerification,
            verifyRequest,
            findingId,
            values,
            chunkedVulnerabilities,
            chunkedVulnerabilities,
            isReattacking
          ),
        ]);
      }
  );

  return requestedChunks.reduce(
    async (previousValue, currentValue): Promise<VerificationResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<VerificationResult[]>([])
  );
};

export {
  getAreAllChunckedMutationValid,
  getAreAllMutationValid,
  handleRequestVerification,
  handleRequestVerificationError,
  handleVerifyRequest,
  handleVerifyRequestError,
  handleAltSubmitHelper,
  handleSubmitHelper,
};
