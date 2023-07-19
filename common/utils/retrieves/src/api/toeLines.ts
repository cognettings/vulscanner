/* eslint-disable fp/no-mutation, fp/no-let */

import type {
  IToeLinesEdge,
  IToeLinesPaginator,
  IToeLinesQuery,
} from "./types";

import { GET_TOE_LINES } from "@retrieves/queries";
import { API_CLIENT, handleGraphQlError } from "@retrieves/utils/apollo";
import { Logger } from "@retrieves/utils/logging";

const getToeLines = async (
  groupName: string,
  rootId: string
): Promise<IToeLinesEdge[]> => {
  let edges: IToeLinesEdge[] = [];
  let hasNextPage = true;
  let endCursor = "";

  // eslint-disable-next-line fp/no-loops
  do {
    // eslint-disable-next-line no-await-in-loop
    const result = await Promise.resolve(
      API_CLIENT.query<IToeLinesQuery>({
        query: GET_TOE_LINES,
        variables: { after: endCursor, first: 500, groupName, rootId },
      })
        .then((_result): IToeLinesPaginator => {
          return _result.data.group.toeLines;
        })
        .catch(async (error): Promise<IToeLinesPaginator> => {
          await handleGraphQlError(error);
          Logger.error(
            `Failed to get ToE Lines from a root in ${groupName}:`,
            error
          );

          return { edges: [], pageInfo: { endCursor: "", hasNextPage: false } };
        })
    );
    edges = [...edges, ...result.edges];
    ({ hasNextPage, endCursor } = result.pageInfo);
  } while (hasNextPage);

  return edges;
};

export { getToeLines };
