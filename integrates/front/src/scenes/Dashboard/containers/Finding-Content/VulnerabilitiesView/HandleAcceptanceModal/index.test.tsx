import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_FINDING_HEADER } from "../../queries";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import {
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "pages/home/dashboard/navbar/breadcrumb/queries";
import { ToDo } from "pages/home/dashboard/navbar/to-do";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { HandleAcceptanceModal } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/index";
import {
  CONFIRM_VULNERABILITIES,
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTANCE,
  REJECT_VULNERABILITIES,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/queries";
import { GET_FINDING_INFO } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_GROUP_VULNERABILITIES } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("handle vulns acceptance modal", (): void => {
  const btnConfirm = "components.modal.confirm";
  const mockedUserAndOrgQueries: MockedResponse[] = [
    {
      request: {
        query: GET_USER_ORGANIZATIONS,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            organizations: [
              {
                __typename: "Organization",
                name: "okada",
              },
              {
                __typename: "Organization",
                name: "bulat",
              },
            ],
            userEmail: "assigned-user-1",
          },
        },
      },
    },
    {
      request: {
        query: GET_ORGANIZATION_GROUP_NAMES,
        variables: {
          organizationId: "okada",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            groups: [
              {
                name: "group1",
              },
              {
                name: "group2",
              },
            ],
            name: "org-test",
          },
        },
      },
    },
    {
      request: {
        query: GET_ORGANIZATION_ID,
        variables: {
          organizationName: "okada",
        },
      },
      result: {
        data: {
          organizationId: {
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: GET_USER_TAGS,
        variables: {
          organizationId: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
        },
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            tags: [{ __typename: "Tag", name: "another-tag" }],
            userEmail: "assigned-user-1",
          },
        },
      },
    },
    {
      request: {
        query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            userEmail: "assigned-user-1",
            vulnerabilitiesAssigned: [],
          },
        },
      },
    },
  ];
  const mockedGroupVulns: MockedResponse = {
    request: {
      query: GET_GROUP_VULNERABILITIES,
      variables: { first: 1200, groupName: "group name" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "group name",
          vulnerabilities: {
            edges: [
              {
                __typename: "VulnerabilityEdge",
                node: {
                  __typename: "Vulnerability",
                  findingId: "438679960",
                  id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
                  state: "VULNERABLE",
                  treatmentAssigned: "test1@fluidattacks.com",
                  where: "This is a test where",
                },
              },
            ],
            pageInfo: {
              endCursor: "test-cursor=",
              hasNextPage: false,
            },
          },
        },
      },
    },
  };

  it("should handle vulns acceptance", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTANCE,
          variables: {
            acceptedVulnerabilities: [],
            findingId: "1",
            justification: "This is a justification test",
            rejectedVulnerabilities: ["test"],
          },
        },
        result: {
          data: { handleVulnerabilitiesAcceptance: { success: true } },
        },
      },
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned: [],
            },
          },
        },
      },
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "1",
          },
        },
        result: {
          data: {
            finding: {
              id: "1",
              releaseDate: "",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "1",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "test",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider
            cache={getCache()}
            mocks={[...mockedUserAndOrgQueries, ...mocksMutation]}
          >
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <ToDo />
              <HandleAcceptanceModal
                findingId={"1"}
                groupName={""}
                handleCloseModal={handleOnClose}
                refetchData={handleRefetchData}
                vulns={mokedVulns}
              />
            </authzGroupContext.Provider>
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "justification" })
      ).toBeInTheDocument();
    });
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a justification test"
    );

    expect(screen.getByRole("checkbox")).toBeChecked();

    await userEvent.click(screen.getByRole("checkbox", { name: "APPROVED" }));

    expect(screen.getByRole("checkbox")).not.toBeChecked();

    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.tabVuln.alerts.acceptanceSuccess",
        "groupAlerts.updatedTitle"
      );
    });

    expect(handleRefetchData).toHaveBeenCalledTimes(1);
    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should handle vulns acceptance errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: HANDLE_VULNS_ACCEPTANCE,
          variables: {
            acceptedVulnerabilities: ["test_error"],
            findingId: "1",
            justification: "This is a justification test error",
            rejectedVulnerabilities: [],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - It cant handle acceptance without being requested"
            ),
          ],
        },
      },
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned: [],
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "1",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "test_error",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider
            cache={getCache()}
            mocks={[...mockedUserAndOrgQueries, ...mocksMutation]}
          >
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <ToDo />
              <HandleAcceptanceModal
                findingId={"1"}
                groupName={""}
                handleCloseModal={jest.fn()}
                refetchData={jest.fn()}
                vulns={mokedVulns}
              />
            </authzGroupContext.Provider>
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "justification" })
      ).toBeInTheDocument();
    });
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a justification test error"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });

    expect(handleRefetchData).not.toHaveBeenCalled();
  });

  it("should handle confirm zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of confirming zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { confirmVulnerabilitiesZeroRisk: { success: true } } },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canRetrieveHacker: false,
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            maxOpenSeverityScore: 0.0,
            minTimeToRemediate: 60,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            status: "VULNERABLE",
            title: "",
            totalOpenCVSSF: 0.0,
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "422286126",
          },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              releaseDate: "2019-05-08",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await userEvent.click(
      within(screen.getByRole("cell", { name: /confirm reject/iu })).getByText(
        /confirm/iu
      )
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of confirming zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "Zero risk vulnerability has been confirmed",
      "Correct!"
    );
  });

  it("should handle confirm zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of confirming zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is not requested"
            ),
          ],
        },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canRetrieveHacker: false,
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            maxOpenSeverityScore: 0.0,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            status: "VULNERABLE",
            title: "",
            totalOpenCVSSF: 0.0,
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "422286126",
          },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              releaseDate: "",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      within(screen.getByRole("cell", { name: /confirm reject/iu })).getByText(
        /confirm/iu
      )
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "justification" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of confirming zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "Zero risk vulnerability is not requested"
      );
    });

    expect(handleRefetchData).not.toHaveBeenCalledTimes(1);
    expect(handleCloseModal).not.toHaveBeenCalledTimes(1);
  });

  it("should handle reject zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REJECT_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of rejecting zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { rejectVulnerabilitiesZeroRisk: { success: true } } },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canRetrieveHacker: false,
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            maxOpenSeverityScore: 0.0,
            minTimeToRemediate: 60,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            status: "VULNERABLE",
            title: "",
            totalOpenCVSSF: 0.0,
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      mockedGroupVulns,
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "422286126",
          },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              releaseDate: "2019-05-08",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      within(screen.getByRole("cell", { name: /confirm reject/iu })).getByText(
        /reject/iu
      )
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "justification" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of rejecting zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "Zero risk vulnerability has been rejected",
      "Correct!"
    );
  });

  it("should handle reject zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REJECT_VULNERABILITIES_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification: "This is a test of rejecting zero risk vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is not requested"
            ),
          ],
        },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canRetrieveHacker: false,
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            maxOpenSeverityScore: 0.0,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            status: "VULNERABLE",
            title: "",
            totalOpenCVSSF: 0.0,
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "422286126",
          },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              releaseDate: "2019-05-08",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      within(screen.getByRole("cell", { name: /confirm reject/iu })).getByText(
        /reject/iu
      )
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "justification" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a test of rejecting zero risk vulns"
    );
    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "Zero risk vulnerability is not requested"
      );
    });

    expect(handleRefetchData).not.toHaveBeenCalledTimes(1);
    expect(handleCloseModal).not.toHaveBeenCalledTimes(1);
  });

  it("should display dropdown to confirm zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
      {
        action: "see_dropdown_to_confirm_zero_risk",
      },
    ]);
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider cache={getCache()}>
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      within(screen.getByRole("cell", { name: /confirm reject/iu })).getByText(
        /confirm/iu
      )
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "justification" })
      ).toBeInTheDocument();
    });
    const expectedDropdownOptionLength: number = 3;

    expect(
      within(
        screen.getByRole("combobox", { name: "justification" })
      ).getAllByRole("option")
    ).toHaveLength(expectedDropdownOptionLength);

    const expectedFpOptionLength: number = 1;
    const expectedOutOfTheScopeOptionLength: number = 1;

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.fn"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.fp"
      )
    ).toHaveLength(expectedFpOptionLength);
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.outOfTheScope"
      )
    ).toHaveLength(expectedOutOfTheScopeOptionLength);
  });

  it("should display dropdown to reject zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_zero_risk_mutate",
      },
      {
        action: "api_mutations_handle_vulnerabilities_acceptance_mutate",
      },
      {
        action: "see_dropdown_to_confirm_zero_risk",
      },
    ]);
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
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
        where: "",
        zeroRisk: "Requested",
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider cache={getCache()}>
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "treatment" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["CONFIRM_REJECT_ZERO_RISK"]
    );

    await userEvent.click(
      within(screen.getByRole("cell", { name: /confirm reject/iu })).getByText(
        /reject/iu
      )
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "justification" })
      ).toBeInTheDocument();
    });
    const expectedDropdownOptionLength: number = 3;

    expect(
      within(
        screen.getByRole("combobox", { name: "justification" })
      ).getAllByRole("option")
    ).toHaveLength(expectedDropdownOptionLength);

    const expectedFnOptionLength: number = 1;
    const expectedComplementaryControlLength: number = 1;

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.fp"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.fn"
      )
    ).toHaveLength(expectedFnOptionLength);
    expect(
      screen.getAllByText(
        "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.complementaryControl"
      )
    ).toHaveLength(expectedComplementaryControlLength);
  });

  it("should handle confirm vulnerability", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: CONFIRM_VULNERABILITIES,
          variables: {
            findingId: "422286126",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { confirmVulnerabilities: { success: true } } },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canRetrieveHacker: false,
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            maxOpenSeverityScore: 0.0,
            minTimeToRemediate: 60,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            status: "VULNERABLE",
            title: "",
            totalOpenCVSSF: 0.0,
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      mockedGroupVulns,
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "422286126",
          },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              releaseDate: "2019-05-08",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
        state: "SUBMITTED",
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
        where: "",
        zeroRisk: null,
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await userEvent.click(
      screen.getByText(
        /searchfindings\.tabvuln\.handleacceptancemodal\.submittedform\.submittedtable\.confirm/iu
      )
    );
    await waitFor((): void => {
      expect(screen.queryByText("components.modal.confirm")).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText("components.modal.confirm"));
    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "Vulnerability has been confirmed",
      "Correct!"
    );
  });

  it("should handle reject vulnerability", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleRefetchData: jest.Mock = jest.fn();
    const handleCloseModal: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      {
        action: "api_mutations_confirm_vulnerabilities_mutate",
      },
      {
        action: "api_mutations_reject_vulnerabilities_mutate",
      },
    ]);
    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: REJECT_VULNERABILITIES,
          variables: {
            findingId: "422286126",
            otherReason: "Other reason test",
            reasons: ["CONSISTENCY", "OTHER"],
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { rejectVulnerabilities: { success: true } } },
      },
    ];
    const mocksFindingHeader: MockedResponse = {
      request: {
        query: GET_FINDING_HEADER,
        variables: {
          canRetrieveHacker: false,
          findingId: "422286126",
        },
      },
      result: {
        data: {
          finding: {
            closedVulns: 0,
            currentState: "CREATED",
            id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
            maxOpenSeverityScore: 0.0,
            minTimeToRemediate: 60,
            openVulns: 0,
            releaseDate: null,
            reportDate: null,
            status: "VULNERABLE",
            title: "",
            totalOpenCVSSF: 0.0,
          },
        },
      },
    };
    const mocksFindingVulnInfo: MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "422286126",
          },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              releaseDate: "2019-05-08",
              remediated: false,
              status: "VULNERABLE",
              totalOpenCVSSF: 0.0,
              verified: false,
            },
          },
        },
      },
    ];
    const mokedVulns: IVulnRowAttr[] = [
      {
        advisories: null,
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "test",
        historicTreatment: [
          {
            acceptanceDate: "",
            acceptanceStatus: "SUBMITTED",
            assigned: "assigned-user-1",
            date: "2019-07-05 09:56:40",
            justification: "test justification",
            treatment: "ACCEPTED_UNDEFINED",
            user: "user@test.com",
          },
        ],
        id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
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
        specific: "",
        state: "SUBMITTED",
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
        where: "",
        zeroRisk: null,
      },
    ];
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mocksFindingHeader,
            ...mocksFindingVulnInfo,
          ]}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "can_report_vulnerabilities" },
                { action: "can_request_zero_risk" },
              ])
            }
          >
            <HandleAcceptanceModal
              findingId={"422286126"}
              groupName={"group name"}
              handleCloseModal={handleCloseModal}
              refetchData={handleRefetchData}
              vulns={mokedVulns}
            />
          </authzGroupContext.Provider>
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );
    await userEvent.click(
      screen.getByText(
        /searchfindings\.tabvuln\.handleacceptancemodal\.submittedform\.submittedtable\.reject/iu
      )
    );
    await userEvent.click(
      within(screen.getByText(/consistency/iu)).getByRole("checkbox", {
        name: /rejectionreasons/iu,
      })
    );
    await userEvent.click(
      within(screen.getByText(/other/iu)).getByRole("checkbox", {
        name: /rejectionreasons/iu,
      })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: /otherrejectionreason/iu }),
      "Other reason test"
    );
    await waitFor((): void => {
      expect(screen.queryByText("components.modal.confirm")).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText("components.modal.confirm"));
    await waitFor((): void => {
      expect(handleRefetchData).toHaveBeenCalledTimes(1);
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(msgSuccess).toHaveBeenCalledWith(
      "Vulnerability has been rejected",
      "Correct!"
    );
  });
});
