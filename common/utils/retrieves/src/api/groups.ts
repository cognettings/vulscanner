import {
  workspace,
  // eslint-disable-next-line import/no-unresolved
} from "vscode";

import type { IGetGroups } from "./types";

import { GET_GROUPS } from "@retrieves/queries";
import type { IOrganization } from "@retrieves/types";
import { API_CLIENT, handleGraphQlError } from "@retrieves/utils/apollo";
import { Logger } from "@retrieves/utils/logging";

const getGroups = async (): Promise<string[]> => {
  const groups: string[] = [
    ...workspace.getConfiguration("fluidattacks").get("extraGroups", []),
    ...(await Promise.resolve(
      API_CLIENT.query({ query: GET_GROUPS })
        .then((result: IGetGroups): string[] =>
          result.data.me.organizations
            .map((org: IOrganization): string[] =>
              org.groups.map((group): string => group.name)
            )
            .flat()
        )
        .catch(async (error): Promise<[]> => {
          await handleGraphQlError(error);
          Logger.error("Failed to get extraGroups: ", error);

          return [];
        })
    )),
  ];

  return groups;
};

export { getGroups };
