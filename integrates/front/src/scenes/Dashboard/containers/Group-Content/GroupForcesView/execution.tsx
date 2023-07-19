import { useQuery } from "@apollo/client";
import type { ColumnDef } from "@tanstack/react-table";
import _ from "lodash";
import React, { useState } from "react";
import ReactAnsi from "react-ansi";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route, Switch } from "react-router-dom";

import { ExecutionDetails } from "./executionDetails";

import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Tab, TabContent, Tabs } from "components/Tabs";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter";
import { GET_FORCES_EXECUTION } from "scenes/Dashboard/containers/Group-Content/GroupForcesView/queries";
import type {
  IExecution,
  IExploitResult,
  IGetForcesExecution,
} from "scenes/Dashboard/containers/Group-Content/GroupForcesView/types";

const Execution: React.FC<IExecution> = (
  props: Readonly<IExecution>
): JSX.Element => {
  const { t } = useTranslation();
  const { log, executionId, groupName } = props;
  const isOld: boolean = log !== undefined;

  const { loading, data } = useQuery<IGetForcesExecution>(
    GET_FORCES_EXECUTION,
    {
      skip: isOld,
      variables: {
        executionId,
        groupName,
      },
    }
  );

  const execution: IExecution = isOld
    ? props
    : { ...props, ...data?.forcesExecution };

  const stateResolve: (status: string) => string = (status: string): string => {
    switch (status) {
      case "OPEN":
        return t("group.forces.status.vulnerable");
      case "CLOSED":
        return t("group.forces.status.secure");
      case "ACCEPTED":
        return t("group.forces.status.accepted");
      default:
        return "";
    }
  };

  const vulns: IExploitResult[] =
    _.isNil(execution.vulnerabilities) ||
    _.isNil(execution.vulnerabilities.open)
      ? []
      : execution.vulnerabilities.open.concat(
          execution.vulnerabilities.closed.concat(
            execution.vulnerabilities.accepted
          )
        );

  const datset = vulns.map(
    (elem: IExploitResult): IExploitResult => ({
      ...elem,
      state: stateResolve(elem.state),
    })
  );

  const columns: ColumnDef<IExploitResult>[] = [
    {
      accessorFn: (row): number => row.exploitability,
      header: t("group.forces.compromisedToe.exploitability"),
      id: "explotability",
    },
    {
      accessorFn: (row): string => row.state,
      cell: (cell: ICellHelper<IExploitResult>): JSX.Element =>
        statusFormatter(cell.getValue()),
      header: t("group.forces.compromisedToe.status"),
      id: "state",
    },
    {
      accessorFn: (row): string => row.kind,
      header: t("group.forces.compromisedToe.type"),
      id: "kind",
    },
    {
      accessorFn: (row): string => row.who,
      header: t("group.forces.compromisedToe.specific"),
      id: "who",
    },
    {
      accessorFn: (row): string => row.where,
      header: t("group.forces.compromisedToe.where"),
      id: "where",
    },
  ];

  const [filters, setFilters] = useState<IFilter<IExploitResult>[]>([
    {
      id: "exploitability",
      key: "exploitability",
      label: t("group.forces.compromisedToe.exploitability"),
      type: "number",
    },
    {
      id: "state",
      key: "state",
      label: t("group.forces.compromisedToe.status"),
      selectOptions: (exploits): string[] =>
        [...new Set(exploits.map((exploit): string => exploit.state))].filter(
          Boolean
        ),
      type: "select",
    },
    {
      id: "kind",
      key: "kind",
      label: t("group.forces.compromisedToe.type"),
      selectOptions: (exploits): string[] =>
        [...new Set(exploits.map((exploit): string => exploit.kind))].filter(
          Boolean
        ),
      type: "select",
    },
    {
      id: "who",
      key: "who",
      label: t("group.forces.compromisedToe.specific"),
      selectOptions: (exploits): string[] =>
        [...new Set(exploits.map((exploit): string => exploit.who))].filter(
          Boolean
        ),
      type: "select",
    },
    {
      id: "where",
      key: "where",
      label: t("group.forces.compromisedToe.where"),
      selectOptions: (exploits): string[] =>
        [...new Set(exploits.map((exploit): string => exploit.where))].filter(
          Boolean
        ),
      type: "select",
    },
  ]);

  const filteredDataset = useFilters(datset, filters);

  if (loading && !isOld) {
    return <p>{"Loading ..."}</p>;
  }

  return (
    <div>
      <ExecutionDetails execution={execution} />
      <br />
      <MemoryRouter initialEntries={["/summary"]} initialIndex={0}>
        <Tabs>
          <Tab
            id={"forcesExecutionSummaryTab"}
            link={"/summary"}
            tooltip={t("group.forces.tabs.summary.tooltip")}
          >
            {t("group.forces.tabs.summary.text")}
          </Tab>
          <Tab
            id={"forcesExecutionLogTab"}
            link={"/log"}
            tooltip={t("group.forces.tabs.log.tooltip")}
          >
            {t("group.forces.tabs.log.text")}
          </Tab>
        </Tabs>
        <TabContent>
          <Switch>
            <Route path={"/summary"}>
              <Table
                columnToggle={true}
                columns={columns}
                data={filteredDataset}
                enableSearchBar={true}
                exportCsv={false}
                filters={
                  <Filters
                    dataset={datset}
                    filters={filters}
                    setFilters={setFilters}
                  />
                }
                id={"tblCompromisedToe"}
              />
            </Route>
            <Route path={"/log"}>
              <ReactAnsi autoScroll={true} log={execution.log as string} />
            </Route>
          </Switch>
        </TabContent>
      </MemoryRouter>
    </div>
  );
};

export { Execution };
