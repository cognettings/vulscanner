import type {
  ApolloError,
  ApolloQueryResult,
  MutationFunction,
  MutationResult,
} from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import { useTranslation } from "react-i18next";

import {
  ADD_ACCESS_TOKEN,
  GET_ACCESS_TOKEN,
  INVALIDATE_ACCESS_TOKEN_MUTATION,
} from "pages/home/dashboard/navbar/user-profile/api-token-modal/queries";
import type {
  IAddAccessTokenAttr,
  IGetAccessTokenAttr,
  IInvalidateAccessTokenAttr,
} from "pages/home/dashboard/navbar/user-profile/api-token-modal/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const useGetAPIToken: () => readonly [
  IGetAccessTokenAttr | undefined,
  () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
] = (): readonly [
  IGetAccessTokenAttr | undefined,
  () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
] => {
  const { t } = useTranslation();

  // Handle query results
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred getting access token", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };

  const { data, refetch } = useQuery<IGetAccessTokenAttr>(GET_ACCESS_TOKEN, {
    fetchPolicy: "network-only",
    onError: handleOnError,
  });

  return [data, refetch] as const;
};

const useAddAccessToken = (
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>
): readonly [MutationFunction, MutationResult<IAddAccessTokenAttr>] => {
  const { t } = useTranslation();

  const [updateAPIToken, mtResponse] = useMutation<IAddAccessTokenAttr>(
    ADD_ACCESS_TOKEN,
    {
      onCompleted: async (mtResult): Promise<void> => {
        if (mtResult.addAccessToken.success) {
          await refetch();
          msgSuccess(
            t("updateAccessToken.successfully"),
            t("updateAccessToken.success")
          );
        }
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          if (error.message === "Exception - Invalid Expiration Time") {
            msgError(t("updateAccessToken.invalidExpTime"));
          } else if (
            error.message ===
            "Exception - Could not add token, maximum number of tokens at the same time is 2"
          ) {
            msgError(t("updateAccessToken.invalidNumberOfAccessTokens"));
          } else {
            Logger.warning("An error occurred adding access token", error);
            msgError(t("groupAlerts.errorTextsad"));
          }
        });
      },
    }
  );

  return [updateAPIToken, mtResponse] as const;
};

const useInvalidateAPIToken = (
  refetch: () => Promise<ApolloQueryResult<IGetAccessTokenAttr>>,
  onClose?: () => void
): MutationFunction => {
  const { t } = useTranslation();

  // Handle mutation results
  const handleOnSuccess: (mtResult: IInvalidateAccessTokenAttr) => void = (
    mtResult: IInvalidateAccessTokenAttr
  ): void => {
    if (mtResult.invalidateAccessToken.success) {
      onClose?.();
      void refetch();
      msgSuccess(
        t("updateAccessToken.delete"),
        t("updateAccessToken.invalidated")
      );
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred invalidating access token", error);
      msgError(t("groupAlerts.errorTextsad"));
    });
  };

  const [invalidateAPIToken] = useMutation(INVALIDATE_ACCESS_TOKEN_MUTATION, {
    onCompleted: handleOnSuccess,
    onError: handleOnError,
  });

  return invalidateAPIToken;
};

export { useAddAccessToken, useGetAPIToken, useInvalidateAPIToken };
