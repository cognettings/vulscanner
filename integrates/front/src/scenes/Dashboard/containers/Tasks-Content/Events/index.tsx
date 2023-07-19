import { useQuery } from "@apollo/client";
import type { ColumnDef, Row } from "@tanstack/react-table";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import type { FormEvent } from "react";
import React, { useCallback, useState } from "react";
import { useHistory } from "react-router-dom";

import { GET_TODO_EVENTS } from "./queries";
import type { IEventAttr, ITodoEvents } from "./types";
import { formatTodoEvents } from "./utils";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { useDebouncedCallback } from "hooks";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";

const tableColumns: ColumnDef<IEventAttr>[] = [
  {
    accessorFn: (row): string => `${row.groupName}`,
    enableColumnFilter: false,
    header: "Group name",
  },
  {
    accessorFn: (row): string | undefined => row.root?.nickname,
    enableColumnFilter: false,
    header: "Root",
  },
  {
    accessorKey: "eventDate",
    filterFn: filterDate,
    header: "Event date",
    meta: { filterType: "dateRange" },
  },
  {
    accessorKey: "detail",
    header: "Description",
  },
  {
    accessorKey: "eventType",
    header: "Type",
    meta: { filterType: "select" },
  },
  {
    accessorKey: "eventStatus",
    cell: (cell: ICellHelper<IEventAttr>): JSX.Element =>
      statusFormatter(cell.getValue()),
    header: "Status",
    meta: { filterType: "select" },
  },
];

const EventsTaskView: React.FC = (): JSX.Element => {
  const { push } = useHistory();
  const { data, refetch } = useQuery<ITodoEvents>(GET_TODO_EVENTS, {
    fetchPolicy: "cache-first",
  });

  const allEvents = data === undefined ? [] : data.me.pendingEvents;
  const Events = formatTodoEvents(allEvents);

  const handleSearch = useDebouncedCallback((search: string): void => {
    void refetch({ search });
  }, 500);

  const [filters, setFilters] = useState<IFilter<IEventAttr>[]>([
    {
      id: "eventDate",
      key: "eventDate",
      label: "Event date",
      type: "dateRange",
    },
    {
      id: "detail",
      key: "detail",
      label: "Description",
      type: "text",
    },
    {
      id: "eventType",
      key: "eventType",
      label: "Type",
      selectOptions: (events: IEventAttr[]): string[] =>
        [...new Set(events.map((event): string => event.eventType))].filter(
          Boolean
        ),
      type: "select",
    },
    {
      id: "eventStatus",
      key: "eventStatus",
      label: "Status",
      selectOptions: (events: IEventAttr[]): string[] =>
        [...new Set(events.map((event): string => event.eventStatus))].filter(
          Boolean
        ),
      type: "select",
    },
  ]);

  const filteredDataset = useFilters(Events, filters);

  const goToEvent = useCallback(
    (rowInfo: Row<IEventAttr>): ((event: FormEvent) => void) => {
      return (event: FormEvent): void => {
        mixpanel.track("ReadEvent");
        push(
          `/groups/${rowInfo.original.groupName}/events/${rowInfo.original.id}/description`
        );
        event.preventDefault();
      };
    },
    [push]
  );

  return (
    <div>
      <Table
        columns={tableColumns}
        data={filteredDataset}
        exportCsv={true}
        filters={
          <Filters dataset={Events} filters={filters} setFilters={setFilters} />
        }
        id={"tblGroupVulnerabilities"}
        onRowClick={goToEvent}
        onSearch={handleSearch}
      />
    </div>
  );
};

export { EventsTaskView };
