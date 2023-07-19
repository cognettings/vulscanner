import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter } from "react-router-dom";

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
import { GET_GROUP_USERS } from "scenes/Dashboard/components/Vulnerabilities/queries";
import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { UpdateDescription } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription";
import {
  REQUEST_VULNS_ZERO_RISK,
  SEND_ASSIGNED_NOTIFICATION,
  UPDATE_VULNERABILITY_MUTATION,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/queries";
import type { IUpdateVulnerabilityResultAttr } from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/types";
import {
  getLastTreatment,
  groupLastHistoricTreatment,
} from "scenes/Dashboard/components/Vulnerabilities/UpdateDescription/utils";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import {
  GET_FINDING_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_ZR_VULNS,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_GROUP_VULNERABILITIES } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Update Description component", (): void => {
  const btnConfirm = "components.modal.confirm";

  const vulns: IVulnDataTypeAttr[] = [
    {
      assigned: "",
      externalBugTrackingSystem: null,
      findingId: "422286126",
      groupName: "testgroupname",
      historicTreatment: [
        {
          date: "",
          justification: "test justification",
          treatment: "UNTREATED",
          user: "",
        },
      ],
      id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
      severity: "2",
      source: "asm",
      specific: "",
      state: "VULNERABLE",
      tag: "one",
      where: "",
    },
  ];
  const mockedQueries: MockedResponse[] = [
    {
      request: {
        query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        variables: {},
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
  const mocksVulns: MockedResponse[] = [
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
    {
      request: {
        query: GET_FINDING_ZR_VULNS,
        variables: {
          canRetrieveZeroRisk: false,
          findingId: "422286126",
          first: 1200,
        },
      },
      result: {
        data: {
          finding: {
            zeroRiskConnection: undefined,
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_NZR_VULNS,
        variables: {
          findingId: "422286126",
          first: 1200,
          state: "VULNERABLE",
        },
      },
      result: {
        data: {
          finding: {
            vulnerabilitiesConnection: {
              edges: [
                {
                  node: {
                    externalBugTrackingSystem: null,
                    findingId: "422286126",
                    id: "",
                    remediated: false,
                    reportDate: "",
                    severity: null,
                    specific: "",
                    state: "VULNERABLE",
                    tag: "",
                    verification: null,
                    vulnerabilityType: "",
                    where: "",
                    zeroRisk: null,
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
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: { first: 1200, groupName: "testgroupname" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "TEST",
            vulnerabilities: {
              edges: [
                {
                  __typename: "VulnerabilityEdge",
                  node: {
                    __typename: "Vulnerability",
                    findingId: "422286126",
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
    },
    ...mockedQueries,
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
          currentState: "APPROVED",
          id: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
          maxOpenSeverityScore: 0.0,
          minTimeToRemediate: 10,
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
  const mocksGroupStakeholder: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_USERS,
        variables: {
          groupName: "testgroupname",
        },
      },
      result: {
        data: {
          group: {
            name: "testgroupname",
            stakeholders: [
              {
                email: "manager_test@test.test",
                invitationState: "REGISTERED",
              },
            ],
          },
        },
      },
    },
  ];

  const mockedUserAndOrgQueries: MockedResponse[] = [
    {
      request: {
        query: GET_USER_ORGANIZATIONS,
        variables: {},
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
            userEmail: "test@fluidattacks.com",
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
            __type: "Organization",
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
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    },
  ];
  const mockedPermissions = new PureAbility<string>([
    { action: "api_mutations_remove_vulnerability_tags_mutate" },
    { action: "api_mutations_request_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_update_vulnerability_treatment_mutate" },
    { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    { action: "api_resolvers_group_stakeholders_resolve" },
  ]);

  it("should group last treatment", (): void => {
    expect.hasAssertions();

    const treatment: IHistoricTreatment = {
      date: "",
      justification: "test justification",
      treatment: "IN PROGRESS",
      user: "",
    };

    const vulnerabilities: IVulnDataTypeAttr[] = [
      {
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "1",
        groupName: "",
        historicTreatment: [treatment],
        id: "test_one",
        severity: null,
        source: "asm",
        specific: "",
        state: "VULNERABLE",
        tag: "one",
        where: "",
      },
      {
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "1",
        groupName: "",
        historicTreatment: [treatment],
        id: "test_two",
        severity: null,
        source: "asm",
        specific: "",
        state: "VULNERABLE",
        tag: "one",
        where: "",
      },
    ];

    const lastTreatment: IHistoricTreatment =
      groupLastHistoricTreatment(vulnerabilities);

    expect(lastTreatment).toStrictEqual(getLastTreatment([treatment]));
  });

  it("list editable fields", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    render(
      <MockedProvider addTypename={false} mocks={mocksGroupStakeholder}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <UpdateDescription
            findingId={"1"}
            groupName={"testgroupname"}
            handleClearSelected={handleClearSelected}
            handleCloseModal={handleOnClose}
            refetchData={handleRefetchData}
            vulnerabilities={vulns}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(screen.queryAllByRole("textbox")).toHaveLength(2);

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["IN_PROGRESS"]
    );
    const numberOfEditableFields: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("textbox")).toHaveLength(
        numberOfEditableFields
      );
    });

    expect(screen.getByRole("spinbutton", { name: "severity" })).toHaveValue(
      Number(vulns[0].severity)
    );
  });

  it("should handle request zero risk", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksMutation: MockedResponse[] = [
      ...mockedUserAndOrgQueries,
      ...mockedQueries,
      ...mocksGroupStakeholder,
      {
        request: {
          query: REQUEST_VULNS_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: { data: { requestVulnerabilitiesZeroRisk: { success: true } } },
      },
      ...mocksVulns,
      ...mockedQueries,
      ...mocksGroupStakeholder,
      mocksFindingHeader,
      ...mockedQueries,
      ...mockedUserAndOrgQueries,
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={mocksMutation}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "can_report_vulnerabilities" },
                  { action: "can_request_zero_risk" },
                ])
              }
            >
              <ToDo />
              <UpdateDescription
                findingId={"422286126"}
                groupName={"testgroupname"}
                handleClearSelected={handleClearSelected}
                handleCloseModal={handleOnClose}
                refetchData={handleRefetchData}
                vulnerabilities={vulns}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["REQUEST_ZERO_RISK"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a commenting test of a request zero risk in vulns"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "Zero risk vulnerability has been requested",
        "Correct!"
      );
    });

    expect(handleClearSelected).toHaveBeenCalledWith();
    expect(handleOnClose).toHaveBeenCalledWith();
    expect(handleRefetchData).toHaveBeenCalledTimes(1);
  });

  it("should handle request zero risk error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksMutation: MockedResponse[] = [
      ...mockedUserAndOrgQueries,
      ...mockedQueries,
      ...mocksGroupStakeholder,
      {
        request: {
          query: REQUEST_VULNS_ZERO_RISK,
          variables: {
            findingId: "422286126",
            justification:
              "This is a commenting test of a request zero risk in vulns",
            vulnerabilities: ["ab25380d-dfe1-4cde-aefd-acca6990d6aa"],
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - Zero risk vulnerability is already requested"
            ),
            new GraphQLError(
              "Exception - Justification must have a maximum of 5000 characters"
            ),
          ],
        },
      },
      ...mockedQueries,
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={mocksMutation}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "can_report_vulnerabilities" },
                  { action: "can_request_zero_risk" },
                ])
              }
            >
              <ToDo />
              <UpdateDescription
                findingId={"422286126"}
                groupName={"testgroupname"}
                handleClearSelected={handleClearSelected}
                handleCloseModal={handleOnClose}
                refetchData={handleRefetchData}
                vulnerabilities={vulns}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["REQUEST_ZERO_RISK"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "This is a commenting test of a request zero risk in vulns"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgError).toHaveBeenNthCalledWith(
        1,
        translate.t("groupAlerts.zeroRiskAlreadyRequested")
      );
    });

    expect(handleClearSelected).not.toHaveBeenCalled();
    expect(handleOnClose).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
    expect(msgError).toHaveBeenNthCalledWith(
      2,
      translate.t("validations.invalidFieldLength")
    );
  });

  it("should render update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();
    const updateTreatment: IUpdateVulnerabilityResultAttr = {
      updateVulnerabilitiesTreatment: { success: true },
      updateVulnerabilityTreatment: { success: true },
    };
    const mutationVariables: Record<
      string,
      boolean | number | string | undefined
    > = {
      acceptanceDate: "",
      assigned: "manager_test@test.test",
      externalBugTrackingSystem: "http://test.t",
      findingId: "422286126",
      isVulnDescriptionChanged: false,
      isVulnTreatmentChanged: true,
      isVulnTreatmentDescriptionChanged: true,
      justification: "test justification to treatment",
      severity: 2,
      source: undefined,
      tag: "one",
      treatment: "IN_PROGRESS",
    };
    const mocksMutation: MockedResponse[] = [
      ...mockedUserAndOrgQueries,
      ...mocksGroupStakeholder,
      ...mockedQueries,
      {
        request: {
          query: UPDATE_VULNERABILITY_MUTATION,
          variables: { ...mutationVariables, vulnerabilityId: "test1" },
        },
        result: { data: updateTreatment },
      },
      {
        request: {
          query: UPDATE_VULNERABILITY_MUTATION,
          variables: { ...mutationVariables, vulnerabilityId: "test2" },
        },
        result: { data: updateTreatment },
      },
      {
        request: {
          query: SEND_ASSIGNED_NOTIFICATION,
          variables: {
            findingId: "422286126",
            vulnerabilities: ["test1", "test2"],
          },
        },
        result: { data: { sendAssignedNotification: { success: true } } },
      },
      ...mockedUserAndOrgQueries,
      ...mocksGroupStakeholder,
      ...mockedQueries,
    ];
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "testgroupname",
        historicTreatment: [],
        id: "test1",
        severity: null,
        source: "asm",
        specific: "",
        state: "VULNERABLE",
        tag: "one",
        where: "",
      },
      {
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "testgroupname",
        historicTreatment: [],
        id: "test2",
        severity: null,
        source: "asm",
        specific: "",
        state: "VULNERABLE",
        tag: "one",
        where: "",
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[...mocksMutation, ...mocksVulns, ...mockedQueries]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <ToDo />
              <UpdateDescription
                findingId={"422286126"}
                groupName={"testgroupname"}
                handleClearSelected={handleClearSelected}
                handleCloseModal={handleOnClose}
                refetchData={handleRefetchData}
                vulnerabilities={vulnsToUpdate}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["IN_PROGRESS"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("combobox", { name: "assigned" })
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "test justification to treatment"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "externalBugTrackingSystem" }),
      "http://test.t"
    );
    await userEvent.type(
      screen.getByRole("spinbutton", { name: "severity" }),
      "2"
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "assigned" }),
      ["manager_test@test.test"]
    );

    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(2);
    });

    expect(handleOnClose).toHaveBeenCalledTimes(1);
  });

  it("should render error update treatment", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClearSelected: jest.Mock = jest.fn();
    const handleOnClose: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksError: MockedResponse = {
      request: {
        query: UPDATE_VULNERABILITY_MUTATION,
        variables: {
          acceptanceDate: "",
          assigned: undefined,
          externalBugTrackingSystem: "",
          findingId: "422286126",
          isVulnDescriptionChanged: false,
          isVulnTreatmentChanged: true,
          isVulnTreatmentDescriptionChanged: false,
          justification: "test justification to treatment",
          severity: -1,
          source: undefined,
          tag: "one",
          treatment: "ACCEPTED_UNDEFINED",
          vulnerabilityId: "test",
        },
      },
      result: {
        errors: [
          new GraphQLError(
            "Vulnerability has been accepted the maximum number of times allowed by the defined policy"
          ),
        ],
      },
    };
    const vulnsToUpdate: IVulnDataTypeAttr[] = [
      {
        assigned: "",
        externalBugTrackingSystem: null,
        findingId: "422286126",
        groupName: "testgroupname",
        historicTreatment: [],
        id: "test",
        severity: null,
        source: "asm",
        specific: "",
        state: "VULNERABLE",
        tag: "one",
        where: "",
      },
    ];
    render(
      <MockedProvider
        addTypename={false}
        mocks={[mocksError, ...mocksGroupStakeholder, ...mocksVulns]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <UpdateDescription
              findingId={"422286126"}
              groupName={"testgroupname"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulnerabilities={vulnsToUpdate}
            />
          </authzGroupContext.Provider>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "treatment" })
      ).toHaveLength(1);
    });

    expect(
      screen.queryByText("searchFindings.tabDescription.approvalTitle")
    ).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "treatment" }),
      ["ACCEPTED_UNDEFINED"]
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "justification" }),
      "test justification to treatment"
    );

    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabDescription.approvalTitle")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      within(
        screen.getByText("searchFindings.tabDescription.approvalMessage")
      ).getByRole("button", { name: btnConfirm })
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        translate.t("searchFindings.tabVuln.alerts.maximumNumberOfAcceptances")
      );
    });

    expect(handleOnClose).not.toHaveBeenCalled();
    expect(handleRefetchData).not.toHaveBeenCalled();
  });

  it("should handle edit source", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleOnClose: jest.Mock = jest.fn();
    const handleClearSelected: jest.Mock = jest.fn();
    const handleRefetchData: jest.Mock = jest.fn();

    const mocksMutation: MockedResponse[] = [
      ...mockedUserAndOrgQueries,
      ...mocksGroupStakeholder,
      ...mockedQueries,
      {
        request: {
          query: UPDATE_VULNERABILITY_MUTATION,
          variables: {
            acceptanceDate: "",
            assigned: undefined,
            externalBugTrackingSystem: "",
            findingId: "422286126",
            isVulnDescriptionChanged: true,
            isVulnTreatmentChanged: false,
            isVulnTreatmentDescriptionChanged: false,
            justification: "",
            severity: 2,
            source: "ANALYST",
            tag: "one",
            treatment: "IN_PROGRESS",
            vulnerabilityId: "ab25380d-dfe1-4cde-aefd-acca6990d6aa",
          },
        },
        result: { data: { updateVulnerabilityDescription: { success: true } } },
      },
      ...mockedUserAndOrgQueries,
      ...mocksGroupStakeholder,
      ...mockedQueries,
    ];
    const mockedSourcePermissions = new PureAbility<string>([
      { action: "see_vulnerability_source" },
      { action: "api_mutations_update_vulnerability_description_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[...mocksMutation, ...mockedQueries]}
        >
          <authzPermissionsContext.Provider value={mockedSourcePermissions}>
            <ToDo />
            <UpdateDescription
              findingId={"422286126"}
              groupName={"testgroupname"}
              handleClearSelected={handleClearSelected}
              handleCloseModal={handleOnClose}
              refetchData={handleRefetchData}
              vulnerabilities={vulns}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("combobox", { name: "source" })
      ).toHaveLength(1);
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "source" }),
      ["ANALYST"]
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenNthCalledWith(
        1,
        "Update vulnerabilities",
        "Congratulations"
      );
    });
  });
});
