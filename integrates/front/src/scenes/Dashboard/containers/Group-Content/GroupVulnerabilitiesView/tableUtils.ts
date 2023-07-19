import type { ColumnDef } from "@tanstack/react-table";

import { requirementsTitleFormatter } from "./formatters/requirementTitleFormatter";

import type { IFilter } from "components/Filter";
import { formatLinkHandler } from "components/Table/formatters/linkFormatter";
import type { ICellHelper } from "components/Table/types";
import { vulnerabilityFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/vulnerabilityFormat";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { filterVerification } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/utils";
import { severityFormatter } from "utils/formatHelpers";
import { translate } from "utils/translations/translate";

const tableColumns: ColumnDef<IVulnRowAttr>[] = [
  {
    accessorKey: "where",
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
      vulnerabilityFormatter({
        reattack: cell.row.original.verification as string,
        source: cell.row.original.vulnerabilityType,
        specific: cell.row.original.specific,
        status: cell.row.original.state,
        treatment: cell.row.original.treatmentStatus,
        where: cell.getValue(),
      }),
    enableColumnFilter: false,
    header: "Vulnerability",
  },
  {
    accessorFn: (row: IVulnRowAttr): string => String(row.finding?.title),
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/description`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Type",
  },
  {
    accessorFn: (row: IVulnRowAttr): string => String(row.requirements),
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
      requirementsTitleFormatter({
        reqsList: cell.row.original.requirements,
      }),
    enableColumnFilter: false,
    header: "Criteria",
  },
  {
    accessorKey: "reportDate",
    enableColumnFilter: false,
    header: "Found",
  },
  {
    accessorFn: (row: IVulnRowAttr): number =>
      Number(row.severityTemporalScore),
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
      severityFormatter(cell.getValue()),
    enableColumnFilter: false,
    header: "Severity",
  },
  {
    accessorFn: (): string => "View",
    cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element => {
      const link = `vulns/${String(cell.row.original.finding?.id)}/evidence`;
      const text = cell.getValue<string>();

      return formatLinkHandler(link, text);
    },
    enableColumnFilter: false,
    header: "Evidence",
  },
];

const tableFilters: IFilter<IVulnRowAttr>[] = [
  {
    id: "root",
    key: "where",
    label: "Root",
    type: "text",
  },
  {
    id: "currentState",
    key: "state",
    label: "Status",
    selectOptions: [
      {
        header: translate.t("searchFindings.header.status.stateLabel.open"),
        value: "VULNERABLE",
      },
      {
        header: translate.t("searchFindings.header.status.stateLabel.closed"),
        value: "SAFE",
      },
      {
        header: translate.t("searchFindings.header.status.stateLabel.rejected"),
        value: "REJECTED",
      },
      {
        header: translate.t(
          "searchFindings.header.status.stateLabel.submitted"
        ),
        value: "SUBMITTED",
      },
    ],
    type: "select",
  },
  {
    id: "type",
    key: "vulnerabilityType",
    label: "Source",
    selectOptions: [
      {
        header: translate.t(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.inputs"
        ),
        value: "INPUTS",
      },
      {
        header: translate.t(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.ports"
        ),
        value: "PORTS",
      },
      {
        header: translate.t(
          "searchFindings.tabVuln.vulnTable.vulnerabilityType.lines"
        ),
        value: "LINES",
      },
    ],
    type: "select",
  },
  {
    id: "treatment",
    key: "treatmentStatus",
    label: "Treatment",
    selectOptions: [
      { header: "In progress", value: "IN_PROGRESS" },
      { header: "Untreated", value: "UNTREATED" },
      { header: "Temporarily accepted", value: "ACCEPTED" },
      { header: "Permanently accepted", value: "ACCEPTED_UNDEFINED" },
    ],
    type: "select",
  },
  {
    id: "verification",
    key: filterVerification,
    label: "Reattack",
    selectOptions: [
      {
        header: "On hold",
        value: "On_hold",
      },
      {
        header: translate.t("searchFindings.tabVuln.requested"),
        value: "Requested",
      },
      {
        header: translate.t("searchFindings.tabVuln.verified"),
        value: "Verified",
      },
      {
        header: translate.t("searchFindings.tabVuln.notRequested"),
        value: "NotRequested",
      },
    ],
    type: "select",
  },
];

export { tableColumns, tableFilters };
