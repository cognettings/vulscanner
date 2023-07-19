import { PureAbility } from "@casl/ability";
import type { ColumnDef } from "@tanstack/react-table";
import { render, screen, within } from "@testing-library/react";
import dayjs from "dayjs";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { statusFormatter } from "./Formatter";
import type { IVulnRowAttr } from "./types";

import { filterDate } from "components/Table/filters/filterFunctions/filterDate";
import type { ICellHelper } from "components/Table/types";
import { authzPermissionsContext } from "context/authz/config";
import { VulnComponent } from "scenes/Dashboard/components/Vulnerabilities";

describe("VulnComponent", (): void => {
  const numberOfDaysOldThanAWeek: number = 12;
  const numberOfDays: number = 5;
  const columns: ColumnDef<IVulnRowAttr>[] = [
    {
      accessorKey: "where",
      enableColumnFilter: false,
    },
    {
      accessorKey: "specific",
      enableColumnFilter: false,
    },
    {
      accessorKey: "state",
      cell: (cell: ICellHelper<IVulnRowAttr>): JSX.Element =>
        statusFormatter(cell.getValue()),
      meta: { filterType: "select" },
    },
    {
      accessorKey: "reportDate",
      filterFn: filterDate,
      meta: { filterType: "dateRange" },
    },
    {
      accessorKey: "verification",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatmentStatus",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "tag",
    },
    {
      accessorKey: "treatmentAcceptanceStatus",
      meta: { filterType: "select" },
    },
    {
      accessorKey: "treatmentAssigned",
      meta: { filterType: "select" },
    },
  ];
  const mockedPermissions = new PureAbility<string>([
    { action: "api_mutations_request_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_update_vulnerability_treatment_mutate" },
    { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
  ]);
  const mocks: IVulnRowAttr[] = [
    {
      advisories: null,
      assigned: "",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          assigned: "assigned-user-1",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          user: "usertreatment@test.test",
        },
      ],
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
      lastStateDate: "2019-07-05 09:56:40",
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: null,
      organizationName: undefined,
      remediated: true,
      reportDate: "",
      rootNickname: "https:",
      severity: "3",
      severityTemporalScore: 3.0,
      source: "asm",
      specific: "specific-1",
      state: "VULNERABLE",
      stream: null,
      tag: "tag-1, tag-2",
      technique: "SCR",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-1",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentStatus: "",
      treatmentUser: "usertreatment@test.test",
      verification: "Requested",
      vulnerabilityType: "inputs",
      where: "https://example.com/inputs",
      zeroRisk: "Requested",
    },
    {
      advisories: null,
      assigned: "",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          assigned: "assigned-user-3",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          user: "usertreatment@test.test",
        },
      ],
      id: "a09c79fc-33fb-4abd-9f20-f3ab1f500bd0",
      lastStateDate: "2019-07-05 09:56:40",
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: dayjs()
        .subtract(numberOfDays, "days")
        .format("YYYY-MM-DD hh:mm:ss"),
      organizationName: undefined,
      remediated: false,
      reportDate: "",
      rootNickname: "https:",
      severity: "1",
      severityTemporalScore: 1.0,
      source: "asm",
      specific: "specific-2",
      state: "SAFE",
      stream: null,
      tag: "tag-5, tag-6",
      technique: "SCR",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-3",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentStatus: "",
      treatmentUser: "usertreatment@test.test",
      verification: "Verified",
      vulnerabilityType: "lines",
      where: "https://example.com/lines",
      zeroRisk: null,
    },
    {
      advisories: null,
      assigned: "assigned-user-4",
      externalBugTrackingSystem: null,
      findingId: "438679960",
      groupName: "test",
      historicTreatment: [
        {
          acceptanceDate: "",
          acceptanceStatus: "",
          assigned: "assigned-user-4",
          date: "2019-07-05 09:56:40",
          justification: "test progress justification",
          treatment: "IN PROGRESS",
          user: "usertreatment@test.test",
        },
      ],
      id: "af7a48b8-d8fc-41da-9282-d424fff563f0",
      lastStateDate: "2019-07-05 09:56:40",
      lastTreatmentDate: "2019-07-05 09:56:40",
      lastVerificationDate: dayjs()
        .subtract(numberOfDaysOldThanAWeek, "days")
        .format("YYYY-MM-DD hh:mm:ss"),
      organizationName: undefined,
      remediated: false,
      reportDate: "",
      rootNickname: "https:",
      severity: "1",
      severityTemporalScore: 1.0,
      source: "asm",
      specific: "specific-3",
      state: "VULNERABLE",
      stream: null,
      tag: "tag-7, tag-8",
      technique: "SCR",
      treatmentAcceptanceDate: "",
      treatmentAcceptanceStatus: "",
      treatmentAssigned: "assigned-user-4",
      treatmentDate: "2019-07-05 09:56:40",
      treatmentJustification: "test progress justification",
      treatmentStatus: "IN PROGRESS",
      treatmentUser: "usertreatment@test.test",
      verification: "Verified",
      vulnerabilityType: "lines",
      where: "https://example.com/lines",
      zeroRisk: null,
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof VulnComponent).toBe("function");
  });

  it("should render in vulnerabilities", (): void => {
    expect.hasAssertions();

    const handleRefetchData: jest.Mock = jest.fn();
    const { rerender } = render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <VulnComponent
            columns={columns}
            extraButtons={<div />}
            findingState={"VULNERABLE"}
            id={"test"}
            isEditing={true}
            isFindingReleased={true}
            isRequestingReattack={false}
            isVerifyingRequest={false}
            onVulnSelect={jest.fn()}
            refetchData={handleRefetchData}
            vulnerabilities={mocks}
          />
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      within(screen.getAllByRole("row")[1]).getByRole("checkbox")
    ).not.toBeDisabled();
    expect(
      within(screen.getAllByRole("row")[3]).getByRole("checkbox")
    ).not.toBeDisabled();

    rerender(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <VulnComponent
            columns={columns}
            extraButtons={<div />}
            findingState={"VULNERABLE"}
            id={"test"}
            isEditing={false}
            isFindingReleased={true}
            isRequestingReattack={true}
            isVerifyingRequest={false}
            onVulnSelect={jest.fn()}
            refetchData={handleRefetchData}
            vulnerabilities={mocks}
          />
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    expect(
      within(screen.getAllByRole("row")[1]).getByRole("checkbox")
    ).toBeDisabled();
    expect(
      within(screen.getAllByRole("row")[3]).getByRole("checkbox")
    ).toBeDisabled();
    expect(handleRefetchData).not.toHaveBeenCalled();
  });

  it("should render in vulnerabilities in draft", (): void => {
    expect.hasAssertions();

    const handleRefetchData: jest.Mock = jest.fn();
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <VulnComponent
            columns={columns}
            extraButtons={<div />}
            findingState={"VULNERABLE"}
            id={"test"}
            isEditing={true}
            isFindingReleased={false}
            isRequestingReattack={false}
            isVerifyingRequest={false}
            onVulnSelect={jest.fn()}
            refetchData={handleRefetchData}
            vulnerabilities={mocks}
          />
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    expect(screen.queryByRole("table")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabDescription.editVuln")
    ).not.toBeInTheDocument();
    expect(screen.queryAllByRole("button")).toHaveLength(1);
    expect(screen.queryAllByRole("checkbox")).toHaveLength(0);
    expect(handleRefetchData).not.toHaveBeenCalled();
  });
});
