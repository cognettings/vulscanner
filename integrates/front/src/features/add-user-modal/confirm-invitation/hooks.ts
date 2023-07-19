import { useQuery } from "@apollo/client";

import type { IGroupBilling, IOrganizationBilling } from "./queries";
import { GET_GROUP_BILLING, GET_ORGANIZATION_BILLING } from "./queries";

import { Logger } from "utils/logger";

const useGroupActors = (groupName?: string): string[] => {
  const { data } = useQuery<IGroupBilling>(GET_GROUP_BILLING, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't get group billing", error);
      });
    },
    skip: groupName === undefined,
    variables: { groupName },
  });

  if (data === undefined) {
    return [];
  }

  const { authors } = data.group.billing;

  return authors.map((author): string => author.actor);
};

const useOrganizationActors = (organizationId?: string): string[] => {
  const { data } = useQuery<IOrganizationBilling>(GET_ORGANIZATION_BILLING, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't get organization billing", error);
      });
    },
    skip: organizationId === undefined,
    variables: { organizationId },
  });

  if (data === undefined) {
    return [];
  }

  const { authors } = data.organization.billing;

  return authors.map((author): string => author.actor);
};

export { useGroupActors, useOrganizationActors };
