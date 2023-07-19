import { useQuery } from "@apollo/client";
import type { ColumnDef, Row } from "@tanstack/react-table";
import _ from "lodash";
import React, { useCallback } from "react";
import { useHistory } from "react-router-dom";

import { Table } from "components/Table";
import { GET_TODO_REATTACKS } from "scenes/Dashboard/containers/Tasks-Content/Reattacks/queries";
import type {
  IFindingFormatted,
  IGetTodoReattacks,
} from "scenes/Dashboard/containers/Tasks-Content/Reattacks/types";
import { formatFindings } from "scenes/Dashboard/containers/Tasks-Content/Reattacks/utils";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import type { IGetUserOrganizationsGroups } from "scenes/Dashboard/types";
import { Logger } from "utils/logger";

export const TasksReattacks: React.FC = (): JSX.Element => {
  const { push } = useHistory();

  const columns: ColumnDef<IFindingFormatted>[] = [
    {
      accessorKey: "groupName",
      header: "Group name",
    },
    {
      accessorKey: "title",
      header: "Type",
    },
    {
      accessorFn: (row: IFindingFormatted): string =>
        row.verificationSummary.requested,
      header: "Requested vulns",
    },
    {
      accessorKey: "oldestReattackRequestedDate",
      header: "Reattack date",
    },
  ];

  const { data: userData } = useQuery<IGetUserOrganizationsGroups>(
    GET_USER_ORGANIZATIONS_GROUPS,
    {
      fetchPolicy: "cache-first",
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          Logger.warning("An error occurred fetching user groups", error);
        });
      },
    }
  );

  const { data, fetchMore } = useQuery<IGetTodoReattacks>(GET_TODO_REATTACKS, {
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        Logger.warning(
          "An error occurred fetching user findings from dashboard",
          error
        );
      });
    },
    skip: _.isUndefined(userData),
    variables: { first: 150 },
  });

  const dataset: IFindingFormatted[] = formatFindings(
    userData === undefined ? [] : userData.me.organizations,
    _.isUndefined(data) || _.isEmpty(data)
      ? []
      : _.flatten(data.me.findingReattacksConnection.edges)
  );

  const handleNextPage = useCallback(async (): Promise<void> => {
    const pageInfo =
      data === undefined
        ? { endCursor: "", hasNextPage: false }
        : data.me.findingReattacksConnection.pageInfo;

    if (pageInfo.hasNextPage) {
      await fetchMore({ variables: { after: pageInfo.endCursor } });
    }
  }, [data, fetchMore]);

  const goToFinding = useCallback(
    (rowInfo: Row<IFindingFormatted>): ((event: React.FormEvent) => void) => {
      const orgName = rowInfo.original.organizationName ?? "";

      return (event: React.FormEvent): void => {
        push(
          `/orgs/${orgName}/groups/${rowInfo.original.groupName}/vulns/${rowInfo.original.id}/locations`
        );
        event.preventDefault();
      };
    },
    [push]
  );

  return (
    <React.StrictMode>
      <Table
        columns={columns}
        data={dataset}
        exportCsv={true}
        id={"tblTodoReattacks"}
        onNextPage={handleNextPage}
        onRowClick={goToFinding}
      />
    </React.StrictMode>
  );
};
