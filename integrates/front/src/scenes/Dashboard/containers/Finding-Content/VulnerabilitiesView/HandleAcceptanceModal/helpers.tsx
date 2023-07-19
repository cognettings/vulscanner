import type {
  ApolloError,
  FetchResult,
  InternalRefetchQueriesInclude,
  MutationFunctionOptions,
  MutationHookOptions,
} from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";

import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import type {
  IAcceptanceVulns,
  IConfirmVulnZeroRiskResultAttr,
  IConfirmVulnerabilitiesResultAttr,
  IRejectVulnerabilitiesResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
  VulnUpdateResult,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";
import { GET_FINDING_INFO } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_GROUP_VULNERABILITIES } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const confirmVulnerabilityHelper = (
  isConfirmRejectVulnerabilitySelected: boolean,
  confirmVulnerabilities: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  confirmedVulns: IVulnRowAttr[]
): void => {
  if (isConfirmRejectVulnerabilitySelected && !_.isEmpty(confirmedVulns)) {
    Object.entries(
      _.groupBy(
        confirmedVulns,
        (vulnerability: IVulnRowAttr): string => vulnerability.findingId
      )
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnRowAttr[]
      ]): Promise<void> => {
        const confirmedVulnIds: string[] = chunkedVulnerabilities.map(
          (vulnerability: IVulnRowAttr): string => vulnerability.id
        );
        await confirmVulnerabilities({
          variables: {
            findingId,
            vulnerabilities: confirmedVulnIds,
          },
        });
      }
    );
  }
};

const confirmVulnerabilityProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  groupName?: string,
  findingId?: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IConfirmVulnerabilitiesResultAttr): void => {
      if (data.confirmVulnerabilities.success) {
        msgSuccess(
          translate.t("groupAlerts.confirmedVulnerabilitySuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - The vulnerability has not been submitted"
        ) {
          msgError(translate.t("groupAlerts.vulnerabilityIsNotSubmitted"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred confirming vulnerability", error);
        }
      });
    },
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_INFO,
              variables: {
                findingId,
              },
            },
            {
              query: GET_FINDING_HEADER,
              variables: {
                findingId,
              },
            },
            ...(groupName === undefined
              ? []
              : [
                  {
                    query: GET_GROUP_VULNERABILITIES,
                    variables: { first: 1200, groupName },
                  },
                ]),
          ],
  };
};

const confirmZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId?: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IConfirmVulnZeroRiskResultAttr): void => {
      if (data.confirmVulnerabilitiesZeroRisk.success) {
        msgSuccess(
          translate.t("groupAlerts.confirmedZeroRiskSuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - Zero risk vulnerability is not requested"
        ) {
          msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred confirming zero risk vuln", error);
        }
      });
    },
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_INFO,
              variables: {
                findingId,
              },
            },
            {
              query: GET_FINDING_HEADER,
              variables: {
                findingId,
              },
            },
          ],
  };
};

const rejectZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  groupName: string,
  findingId?: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IRejectZeroRiskVulnResultAttr): void => {
      if (data.rejectVulnerabilitiesZeroRisk.success) {
        msgSuccess(
          translate.t("groupAlerts.rejectedZeroRiskSuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - Zero risk vulnerability is not requested"
        ) {
          msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred rejecting zero risk vuln", error);
        }
      });
    },
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_INFO,
              variables: {
                findingId,
              },
            },
            {
              query: GET_FINDING_HEADER,
              variables: {
                findingId,
              },
            },
            {
              query: GET_GROUP_VULNERABILITIES,
              variables: {
                first: 1200,
                groupName,
              },
            },
          ],
  };
};

const handleSubmitHelper = async (
  handleAcceptance: (
    variables: Record<string, unknown>
  ) => Promise<VulnUpdateResult>,
  findingId: string,
  values: { justification: string },
  vulnerabilitiesList: IAcceptanceVulns[]
): Promise<VulnUpdateResult[]> => {
  const maxChunkSize = 64;
  const minChunkSize = 16;
  const VulnerabilitiesListChunks: IAcceptanceVulns[][] = _.chunk(
    vulnerabilitiesList,
    maxChunkSize
  );
  const acceptanceChunks = VulnerabilitiesListChunks.map(
    (chunkedVulnerabilitiesList): (() => Promise<VulnUpdateResult[]>) =>
      async (): Promise<VulnUpdateResult[]> => {
        const chunckedVulnerabilities: IAcceptanceVulns[][] = _.chunk(
          chunkedVulnerabilitiesList,
          minChunkSize
        );
        const allPromises = chunckedVulnerabilities.map(
          async (chunkedVulns): Promise<VulnUpdateResult> => {
            const approvedVulnsId: string[] = chunkedVulns.reduce(
              (acc: string[], vuln: IAcceptanceVulns): string[] =>
                vuln.acceptanceStatus === "APPROVED" ? [...acc, vuln.id] : acc,
              []
            );
            const rejectedVulnsId: string[] = chunkedVulns.reduce(
              (acc: string[], vuln: IAcceptanceVulns): string[] =>
                vuln.acceptanceStatus === "REJECTED" ? [...acc, vuln.id] : acc,
              []
            );

            return handleAcceptance({
              variables: {
                acceptedVulnerabilities: approvedVulnsId,
                findingId,
                justification: values.justification,
                rejectedVulnerabilities: rejectedVulnsId,
              },
            });
          }
        );

        return Promise.all(allPromises);
      }
  );

  return acceptanceChunks.reduce(
    async (previousValue, currentValue): Promise<VulnUpdateResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<VulnUpdateResult[]>([])
  );
};

const isAcceptedUndefinedSelectedHelper = async (
  handleAcceptance: (
    variables: Record<string, unknown>
  ) => Promise<VulnUpdateResult>,
  acceptedVulns: IVulnDataAttr[],
  values: {
    justification: string;
  },
  rejectedVulns: IVulnDataAttr[]
): Promise<VulnUpdateResult[][]> => {
  const vulnerabilitiesList = [...acceptedVulns, ...rejectedVulns];
  const acceptedVulnsIds = acceptedVulns.map(
    (vuln: IVulnDataAttr): string => vuln.id
  );
  const vulnerabilitiesByFinding = _.groupBy(
    vulnerabilitiesList,
    (vuln: IVulnDataAttr): string => vuln.findingId
  );
  const acceptanceChunks = Object.entries(vulnerabilitiesByFinding).map(
    ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): (() => Promise<VulnUpdateResult[][]>) =>
      async (): Promise<VulnUpdateResult[][]> => {
        return Promise.all([
          handleSubmitHelper(
            handleAcceptance,
            findingId,
            values,
            chunkedVulnerabilities.map(
              (vuln: IVulnDataAttr): IAcceptanceVulns => ({
                ...vuln,
                acceptanceStatus: _.includes(acceptedVulnsIds, vuln.id)
                  ? "APPROVED"
                  : "REJECTED",
              })
            )
          ),
        ]);
      }
  );

  return acceptanceChunks.reduce(
    async (previousValue, currentValue): Promise<VulnUpdateResult[][]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<VulnUpdateResult[][]>([])
  );
};

const isConfirmZeroRiskSelectedHelper = (
  isConfirmZeroRiskSelected: boolean,
  confirmZeroRisk: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  acceptedVulns: IVulnDataAttr[],
  values: {
    justification: string;
  }
): void => {
  if (isConfirmZeroRiskSelected && !_.isEmpty(acceptedVulns)) {
    Object.entries(
      _.groupBy(acceptedVulns, (vuln: IVulnDataAttr): string => vuln.findingId)
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): Promise<void> => {
        const acceptedVulnIds: string[] = chunkedVulnerabilities.map(
          (vuln: IVulnDataAttr): string => vuln.id
        );
        await confirmZeroRisk({
          variables: {
            findingId,
            justification: values.justification,
            vulnerabilities: acceptedVulnIds,
          },
        });
      }
    );
  }
};

const isRejectZeroRiskSelectedHelper = (
  isRejectZeroRiskSelected: boolean,
  rejectZeroRisk: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  values: {
    justification: string;
  },
  rejectedVulns: IVulnDataAttr[]
): void => {
  if (isRejectZeroRiskSelected && !_.isEmpty(rejectedVulns)) {
    Object.entries(
      _.groupBy(rejectedVulns, (vuln: IVulnDataAttr): string => vuln.findingId)
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): Promise<void> => {
        const rejectedVulnIds: string[] = chunkedVulnerabilities.map(
          (vuln: IVulnDataAttr): string => vuln.id
        );
        await rejectZeroRisk({
          variables: {
            findingId,
            justification: values.justification,
            vulnerabilities: rejectedVulnIds,
          },
        });
      }
    );
  }
};

const rejectVulnerabilityHelper = (
  isConfirmRejectVulnerabilitySelected: boolean,
  rejectVulnerabilities: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  values: {
    reasons: string[];
    otherReason?: string;
  },
  rejectedVulns: IVulnRowAttr[]
): void => {
  if (isConfirmRejectVulnerabilitySelected && !_.isEmpty(rejectedVulns)) {
    Object.entries(
      _.groupBy(
        rejectedVulns,
        (vulnerability: IVulnRowAttr): string => vulnerability.findingId
      )
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnRowAttr[]
      ]): Promise<void> => {
        const rejectedVulnIds: string[] = chunkedVulnerabilities.map(
          (vulnerability: IVulnRowAttr): string => vulnerability.id
        );
        await rejectVulnerabilities({
          variables: {
            findingId,
            otherReason: values.otherReason,
            reasons: values.reasons,
            vulnerabilities: rejectedVulnIds,
          },
        });
      }
    );
  }
};

const rejectVulnerabilityProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId?: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IRejectVulnerabilitiesResultAttr): void => {
      if (data.rejectVulnerabilities.success) {
        msgSuccess(
          translate.t("groupAlerts.rejectedVulnerabilitySuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - Zero risk vulnerability is not requested"
        ) {
          msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred confirming zero risk vuln", error);
        }
      });
    },
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_INFO,
              variables: {
                findingId,
              },
            },
            {
              query: GET_FINDING_HEADER,
              variables: {
                findingId,
              },
            },
          ],
  };
};

const addObservationRejectionProps = (type: string): MutationHookOptions => {
  return {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (error.message === "Exception - Invalid field length in form") {
          msgError(translate.t("validations.invalidFieldLength"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(`An error occurred posting ${type}`, graphQLErrors);
        }
      });
    },
  };
};

const addObservationHelper = (
  addComment: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  values: {
    justification?: string;
    parentComment: number;
  },
  type: string,
  rejectedVulns: IVulnRowAttr[],
  findingId?: string
): void => {
  if (values.justification !== undefined) {
    const wheres: string[] = rejectedVulns.map((vuln): string => {
      return ` - ${vuln.where} (${vuln.specific})`;
    });
    const concatenatedWheres: string = wheres.join("");
    const formattedObservation: string = `Regarding vulnerabilities: \n${concatenatedWheres}\n\nJustification:\n  ${values.justification}`;
    void addComment({
      variables: {
        content: formattedObservation,
        findingId,
        parentComment: values.parentComment,
        type,
      },
    });
  }
};

export {
  addObservationHelper,
  addObservationRejectionProps,
  confirmVulnerabilityProps,
  confirmZeroRiskProps,
  confirmVulnerabilityHelper,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  rejectVulnerabilityHelper,
  rejectVulnerabilityProps,
  rejectZeroRiskProps,
};
