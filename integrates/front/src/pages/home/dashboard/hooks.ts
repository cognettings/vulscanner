import { useQuery } from "@apollo/client";
import { useEffect } from "react";
import { useHistory } from "react-router-dom";

import { GET_USER_ORGANIZATIONS } from "./navbar/breadcrumb/queries";
import type { IUserOrganizations } from "./navbar/breadcrumb/queries";

import { Logger } from "utils/logger";

/** Determines the organization to show by default  */
const useInitialOrganization = (): string | undefined => {
  const { data } = useQuery<IUserOrganizations>(GET_USER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.error("Couldn't get user organizations", error);
      });
    },
  });

  // Attempt 1: Get it from last organization
  const lastOrganization = localStorage.getItem("organization");

  if (lastOrganization !== null) {
    const storedData: { name?: string } = JSON.parse(lastOrganization);

    if (storedData.name !== undefined) {
      return storedData.name;
    }
  }

  // Attempt 2: Get it from user organizations
  if (data === undefined) {
    return undefined;
  }

  return data.me.organizations[0].name;
};

/** Applies the start url set by the backend */
const useStartUrl = (): void => {
  const { push } = useHistory();

  useEffect((): void => {
    const startUrl = localStorage.getItem("start_url");

    if (startUrl !== null) {
      localStorage.removeItem("start_url");
      push(startUrl);
    }
  }, [push]);
};

export { useInitialOrganization, useStartUrl };
