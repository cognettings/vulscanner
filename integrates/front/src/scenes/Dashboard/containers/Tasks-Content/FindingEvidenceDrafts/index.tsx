import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import React, { useCallback } from "react";

import { GET_FINDING_EVIDENCE_DRAFTS } from "./queries";
import type { IFinding, IFindingEvidenceDrafts } from "./types";

import { Table } from "components/Table";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import { Logger } from "utils/logger";

const columns: ColumnDef<IFinding>[] = [
  {
    accessorKey: "groupName",
    cell: (cell): JSX.Element => {
      const { groupName } = cell.row.original;
      const link = `../groups/${groupName}`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Group name",
  },
  {
    accessorKey: "title",
    cell: (cell): JSX.Element => {
      const { groupName, id } = cell.row.original;
      const link = `../groups/${groupName}/vulns/${id}/evidence`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    header: "Type",
  },
];

export const FindingEvidenceDrafts: React.FC = (): JSX.Element => {
  const { data, fetchMore } = useQuery<IFindingEvidenceDrafts>(
    GET_FINDING_EVIDENCE_DRAFTS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.error(
            "An error occurred loading finding evidence drafts",
            error
          );
        });
      },
      pollInterval: 5000,
      variables: { first: 100 },
    }
  );

  const loadNextPage = useCallback(
    (endCursor: string): (() => Promise<void>) => {
      return async (): Promise<void> => {
        await fetchMore({ variables: { after: endCursor } });
      };
    },
    [fetchMore]
  );

  if (data === undefined) {
    return <div />;
  }

  const { edges, pageInfo } = data.me.findingEvidenceDrafts;
  const findings = edges.map((edge): IFinding => edge.node);

  return (
    <div>
      <Table
        columns={columns}
        data={findings}
        hasNextPage={pageInfo.hasNextPage}
        id={"findingEvidenceDraftsTable"}
        onNextPage={loadNextPage(pageInfo.endCursor)}
      />
    </div>
  );
};
