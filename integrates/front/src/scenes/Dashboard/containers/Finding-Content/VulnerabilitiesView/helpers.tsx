import type {
  ApolloError,
  InternalRefetchQueriesInclude,
  MutationHookOptions,
} from "@apollo/client";
import type { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";

import { GET_FINDING_INFO } from "./queries";
import type {
  ICloseVulnerabilitiesResultAttr,
  IResubmitVulnerabilitiesResultAttr,
} from "./types";

import { GET_GROUP_VULNERABILITIES } from "../../Group-Content/GroupFindingsView/queries";
import { GET_FINDING_HEADER } from "../queries";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const resubmitVulnerabilityProps = (
  groupName: string,
  findingId: string,
  refetchData: () => void
): MutationHookOptions => {
  return {
    onCompleted: (data: IResubmitVulnerabilitiesResultAttr): void => {
      if (data.resubmitVulnerabilities.success) {
        msgSuccess(
          translate.t("groupAlerts.submittedVulnerabilitySuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred resubmitting vulnerability", error);
      });
    },
    refetchQueries: (): InternalRefetchQueriesInclude => [
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
        variables: { first: 1200, groupName },
      },
    ],
  };
};

type CloseVulnerabilitiesResult =
  ExecutionResult<ICloseVulnerabilitiesResultAttr>;

const isSuccessful = (results: CloseVulnerabilitiesResult[]): boolean[] => {
  return results.map((result): boolean =>
    Boolean(result.data?.closeVulnerabilities.success)
  );
};

const areAllSuccessful = (results: CloseVulnerabilitiesResult[][]): boolean[] =>
  results
    .map(isSuccessful)
    .reduce(
      (previous: boolean[], current: boolean[]): boolean[] => [
        ...previous,
        ...current,
      ],
      []
    );

const handleCloseVulnerabilitiesAux = async (
  closeVulnerabilities: (
    variables: Record<string, unknown>
  ) => Promise<CloseVulnerabilitiesResult>,
  findingId: string,
  vulnerabilities: string[]
): Promise<CloseVulnerabilitiesResult[]> => {
  const chunkSize = 64;
  const vulnChunks = _.chunk(vulnerabilities, chunkSize);
  const closedChunks = vulnChunks.map(
    (chunk): (() => Promise<CloseVulnerabilitiesResult[]>) =>
      async (): Promise<CloseVulnerabilitiesResult[]> =>
        Promise.all([
          closeVulnerabilities({
            variables: {
              findingId,
              vulnerabilities: chunk,
            },
          }),
        ])
  );

  return closedChunks.reduce(
    async (
      previousValue,
      currentValue
    ): Promise<CloseVulnerabilitiesResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<CloseVulnerabilitiesResult[]>([])
  );
};

const handleCloseVulnerabilities = async (
  closeVulnerabilities: (
    variables: Record<string, unknown>
  ) => Promise<CloseVulnerabilitiesResult>,
  vulnerabilities: IVulnRowAttr[]
): Promise<CloseVulnerabilitiesResult[][]> => {
  const vulnerabilitiesByFinding = _.groupBy(
    vulnerabilities,
    (vuln: IVulnRowAttr): string => vuln.findingId
  );
  const closedChunks = Object.entries(vulnerabilitiesByFinding).map(
    ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnRowAttr[]
      ]): (() => Promise<CloseVulnerabilitiesResult[][]>) =>
      async (): Promise<CloseVulnerabilitiesResult[][]> => {
        return Promise.all([
          handleCloseVulnerabilitiesAux(
            closeVulnerabilities,
            findingId,
            chunkedVulnerabilities.map((vuln): string => vuln.id)
          ),
        ]);
      }
  );

  return closedChunks.reduce(
    async (
      previousValue,
      currentValue
    ): Promise<CloseVulnerabilitiesResult[][]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<CloseVulnerabilitiesResult[][]>([])
  );
};

export {
  resubmitVulnerabilityProps,
  areAllSuccessful,
  handleCloseVulnerabilities,
};
