import type { ApolloError } from "@apollo/client";

import {
  ACCEPT_VULNERABILITY_TEMPORARY,
  REQUEST_VULNERABILITIES_VERIFICATION,
} from "@retrieves/queries";
import { API_CLIENT, handleGraphQlError } from "@retrieves/utils/apollo";
import { Logger } from "@retrieves/utils/logging";

interface IRequestReattackData {
  requestVulnerabilitiesVerification: { success: boolean; message?: string };
}

interface IRequestReattackRespose {
  data: IRequestReattackData;
}
interface IAcceptVulnerabilityData {
  updateVulnerabilitiesTreatment: { success: boolean; message?: string };
}

interface IAcceptVulnerabilityResponse {
  data: IAcceptVulnerabilityData;
}

const requestReattack = async (
  findingId: string,
  justification: string,
  vulnerabilities: string[]
): Promise<IRequestReattackData> => {
  const result: IRequestReattackData = (
    await API_CLIENT.mutate({
      mutation: REQUEST_VULNERABILITIES_VERIFICATION,
      variables: {
        findingId,
        justification,
        vulnerabilities,
      },
    }).catch(async (error: ApolloError): Promise<IRequestReattackRespose> => {
      await handleGraphQlError(error);
      Logger.error(`Failed to request reattack:`, error);

      return {
        data: {
          requestVulnerabilitiesVerification: {
            message: error.message,
            success: false,
          },
        },
      };
    })
  ).data;

  return result;
};

const acceptVulnerabilityTemporary = async (
  findingId: string,
  vulnerabilityId: string,
  acceptanceDate: string,
  justification: string,
  treatment: string
): Promise<IAcceptVulnerabilityData> => {
  const result: IAcceptVulnerabilityData = (
    await API_CLIENT.mutate({
      mutation: ACCEPT_VULNERABILITY_TEMPORARY,
      variables: {
        acceptanceDate,
        findingId,
        justification,
        treatment,
        vulnerabilityId,
      },
    }).catch(
      async (error: ApolloError): Promise<IAcceptVulnerabilityResponse> => {
        await handleGraphQlError(error);
        Logger.error(`Failed to accept vulns:`, error);

        return {
          data: {
            updateVulnerabilitiesTreatment: {
              message: error.message,
              success: false,
            },
          },
        };
      }
    )
  ).data;

  return result;
};

export { requestReattack, acceptVulnerabilityTemporary };
export type { IAcceptVulnerabilityData };
