import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { GET_GROUP_SERVICES } from "hooks/queries";
import {
  GET_STAKEHOLDER_PHONE,
  VERIFY_STAKEHOLDER_MUTATION,
} from "scenes/Dashboard/components/VerifyDialog/queries";
import { GET_LANGUAGE } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/queries";
import { GroupFindingsView } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView";
import {
  ADD_FINDING_MUTATION,
  GET_FINDINGS,
  GET_GROUP_VULNERABILITIES,
  GET_ROOTS,
  REQUEST_GROUP_REPORT,
} from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { ReportsModal } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/reportsModal";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("groupFindingsView", (): void => {
  const apolloDataFinding = {
    group: {
      __typename: "Group",
      businessId: "id",
      businessName: "name",
      description: "description",
      findings: [
        {
          __typename: "Finding",
          age: 252,
          closedVulnerabilities: 6,
          description: "This is a test description",
          id: "438679960",
          isExploitable: true,
          lastVulnerability: 33,
          maxOpenSeverityScore: 2.9,
          minTimeToRemediate: 60,
          openAge: 60,
          openVulnerabilities: 6,
          releaseDate: null,
          status: "VULNERABLE",
          title: "038. Business information leak",
          totalOpenCVSSF: 1.308,
          treatment: ["IN PROGRESS"],
          treatmentSummary: {
            accepted: 0,
            acceptedUndefined: 0,
            inProgress: 0,
            untreated: 1,
          },
          verificationSummary: {
            onHold: 1,
            requested: 2,
            verified: 3,
          },
          verified: false,
        },
      ],
      hasMachine: false,
      name: "TEST",
      userRole: "user-role",
    },
  };

  const apolloDataMock: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          groupName: "TEST",
        },
      },
      result: {
        data: apolloDataFinding,
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: "" },
          groupName: "TEST",
        },
      },
      result: {
        data: apolloDataFinding,
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: undefined },
          groupName: "TEST",
        },
      },
      result: {
        data: apolloDataFinding,
      },
    },
    {
      request: {
        query: GET_ROOTS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "TEST",
            roots: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_LANGUAGE,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            language: "EN",
            name: "TEST",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "TEST",
            serviceAttributes: [],
          },
        },
      },
    },
  ];

  const mockStakeholderPhone: MockedResponse = {
    request: {
      query: GET_STAKEHOLDER_PHONE,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          phone: {
            callingCountryCode: "1",
            countryCode: "US",
            nationalNumber: "1234545",
          },
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };
  const mocksMutation: readonly MockedResponse[] = [
    {
      request: {
        query: VERIFY_STAKEHOLDER_MUTATION,
      },
      result: { data: { verifyStakeholder: { success: true } } },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: "" },
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: undefined },
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  const mocksGroupFindings = {
    group: {
      __typename: "Group",
      businessId: "14441323",
      businessName: "Testing Company and Sons",
      description: "Integrates unit test group",
      findings: [
        {
          __typename: "Finding",
          age: 252,
          closedVulnerabilities: 6,
          description: "Test description",
          id: "438679960",
          isExploitable: true,
          lastVulnerability: 5,
          maxOpenSeverityScore: 2.9,
          minTimeToRemediate: 60,
          openAge: 60,
          openVulnerabilities: 6,
          releaseDate: null,
          status: "VULNERABLE",
          title: "038. Business information leak",
          totalOpenCVSSF: 1.308,
          treatment: ["IN PROGRESS"],
          treatmentSummary: {
            accepted: 0,
            acceptedUndefined: 0,
            inProgress: 0,
            untreated: 1,
          },
          verificationSummary: {
            onHold: 1,
            requested: 2,
            verified: 3,
          },
          verified: false,
        },
      ],
      hasMachine: true,
      name: "TEST",
      userRole: "admin",
    },
  };

  const mocksFindings: MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          groupName: "TEST",
        },
      },
      result: {
        data: mocksGroupFindings,
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: "" },
          groupName: "TEST",
        },
      },
      result: {
        data: mocksGroupFindings,
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: undefined },
          groupName: "TEST",
        },
      },
      result: {
        data: mocksGroupFindings,
      },
    },
  ];
  const mocksLocations: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: { first: 1200, groupName: "TEST" },
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
    },
  ];

  const mockReportError: MockedResponse = {
    request: {
      query: REQUEST_GROUP_REPORT,
      variables: {
        groupName: "testgroup",
        reportType: "PDF",
        verificationCode: "1234",
      },
    },
    result: {
      errors: [
        new GraphQLError(
          "Exception - The user already has a requested report for the same group"
        ),
      ],
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupFindingsView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/vulns"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={apolloDataMock}
        >
          <Route
            component={GroupFindingsView}
            path={"/orgs/:organizationName/groups/:groupName"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });
  });

  it("should render report modal and mock request error", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const handleClose: jest.Mock = jest.fn();
    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...apolloDataMock,
            ...mocksMutation,
            mockStakeholderPhone,
            mockReportError,
          ]}
        >
          <Route path={"/orgs/:organizationName/groups/:groupName/vulns"}>
            <ReportsModal
              enableCerts={true}
              isOpen={true}
              onClose={handleClose}
              typesOptions={[]}
              userRole={"user_manager"}
            />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.getByText("group.findings.report.pdf")).toBeInTheDocument();
    });

    // Find buttons
    const buttons: HTMLElement[] = screen.getAllByRole("button", {
      hidden: true,
    });

    [
      "xmark",
      "file-contract",
      "file-pdf",
      "file-excel",
      "sliders",
      "file-zipper",
    ].forEach((expectedDataIcon, idx): void => {
      expect(buttons[idx].querySelector(".svg-inline--fa")).toHaveAttribute(
        "data-icon",
        expectedDataIcon
      );
    });

    await waitFor((): void => {
      expect(
        screen.getByText("group.findings.report.modalTitle")
      ).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.findings.report.pdf"));
    await userEvent.type(
      screen.getByRole("textbox", {
        name: "verificationCode",
      }),
      "1234"
    );
    await userEvent.click(screen.getByText("verifyDialog.verify"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith(
        "groupAlerts.reportAlreadyRequested"
      );
    });
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/vulns"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mockError,
            apolloDataMock[3],
            apolloDataMock[4],
            apolloDataMock[5],
            ...mockError,
          ]}
        >
          <Route
            component={GroupFindingsView}
            path={"/orgs/:organizationName/groups/:groupName"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });
  });

  it("should display all finding columns", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/vulns"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mocksLocations,
            ...mocksFindings,
            apolloDataMock[3],
            apolloDataMock[4],
            apolloDataMock[5],
          ]}
        >
          <Route
            component={GroupFindingsView}
            path={"/orgs/:organizationName/groups/:groupName"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("038. Business information leak")
      ).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("Where")).not.toBeInTheDocument();
    expect(screen.queryByText("Reattack")).not.toBeInTheDocument();
    expect(
      screen.queryByText("test1@fluidattacks.com")
    ).not.toBeInTheDocument();

    await userEvent.click(screen.getByText("group.findings.tableSet.btn.text"));

    await userEvent.click(
      screen.getByRole("checkbox", { checked: false, name: "reattack" })
    );

    await userEvent.type(
      screen.getByText("group.findings.tableSet.modalTitle"),
      "{Escape}"
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.tableSet.modalTitle")
      ).not.toBeInTheDocument();
    });

    expect(screen.getByText("New")).toBeInTheDocument();
    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Severity")).toBeInTheDocument();
    expect(screen.getByText("Open vulnerabilities")).toBeInTheDocument();
    expect(screen.getByText("Last report")).toBeInTheDocument();
    expect(screen.getByText("Reattack")).toBeInTheDocument();

    expect(
      screen.getByText("038. Business information leak")
    ).toBeInTheDocument();
    expect(
      screen.getByText("group.findings.description.value")
    ).toBeInTheDocument();
    expect(screen.getByText("Vulnerable")).toBeInTheDocument();
    expect(screen.getByText("2.9")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
    expect(screen.getByText("Pending")).toBeInTheDocument();
  });

  it("should add finding", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFetch: FetchMockStatic = fetch as FetchMockStatic &
      typeof fetch;
    const baseUrl: string =
      "https://gitlab.com/api/v4/projects/20741933/repository/files";
    const branchRef: string = "trunk";
    const vulnsFileId: string =
      "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
    mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
      body: {
        "001": {
          en: {
            description: "Description.\n",
            impact: "",
            recommendation: "Recommendation.\n",
            threat: "Threat.\n",
            title: "Title test",
          },
          requirements: ["1111", "2222"],
          score: {
            base: {
              // eslint-disable-next-line camelcase
              attack_complexity: "L",
              // eslint-disable-next-line camelcase
              attack_vector: "N",
              availability: "N",
              confidentiality: "N",
              integrity: "L",
              // eslint-disable-next-line camelcase
              privileges_required: "N",
              // eslint-disable-next-line camelcase
              scope: "U",
              // eslint-disable-next-line camelcase
              user_interaction: "N",
            },
            temporal: {
              // eslint-disable-next-line camelcase
              exploit_code_maturity: "P",
              // eslint-disable-next-line camelcase
              remediation_level: "O",
              // eslint-disable-next-line camelcase
              report_confidence: "R",
            },
          },
        },
      },
      status: 200,
    });
    const mockedMutations: readonly MockedResponse[] = [
      {
        request: {
          query: ADD_FINDING_MUTATION,
          variables: {
            attackComplexity: 0,
            attackVector: 0,
            attackVectorDescription: "",
            availabilityImpact: 0,
            availabilityRequirement: 0,
            confidentialityImpact: 0,
            confidentialityRequirement: 0,
            cvssVector:
              "CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:N/E:H/RL:U/RC:R/CR:X/IR:X/AR:X/MAV:X/MAC:X/MPR:X/MUI:X/MS:X/MC:X/MI:X/MA:X",
            description: "Description.\n",
            exploitability: 0,
            groupName: "TEST",
            integrityImpact: 0,
            integrityRequirement: 0,
            minTimeToRemediate: null,
            modifiedAttackComplexity: 0,
            modifiedAttackVector: 0,
            modifiedAvailabilityImpact: 0,
            modifiedConfidentialityImpact: 0,
            modifiedIntegrityImpact: 0,
            modifiedPrivilegesRequired: 0,
            modifiedSeverityScope: 0,
            modifiedUserInteraction: 0,
            privilegesRequired: 0,
            recommendation: "Recommendation.\n",
            remediationLevel: 0,
            reportConfidence: 0,
            severityScope: 0,
            threat: "Threat.\n",
            title: "001. Title test",
            unfulfilledRequirements: ["1111", "2222"],
            userInteraction: 0,
          },
        },
        result: { data: { addFinding: { success: true } } },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_finding_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/vulns"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <MockedProvider
              addTypename={true}
              cache={getCache()}
              mocks={[...apolloDataMock, ...mockedMutations, ...apolloDataMock]}
            >
              <Route
                component={GroupFindingsView}
                path={"/orgs/:organizationName/groups/:groupName"}
              />
            </MockedProvider>
          </authzGroupContext.Provider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByRole("button", {
          name: "group.findings.buttons.add.text",
        })
      ).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: "group.findings.buttons.add.text",
      })
    );

    await waitFor(
      (): void => {
        expect(
          screen.queryByRole("combobox", { name: /title/iu })
        ).toBeInTheDocument();
      },
      { timeout: 5000 }
    );

    await userEvent.type(
      screen.getByRole("combobox", { name: /title/iu }),
      "001. Title test"
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "exploitability" }),
      ["searchFindings.tabSeverity.exploitability.options.high.label"]
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "integrityImpact" }),
      ["searchFindings.tabSeverity.integrityImpact.options.none.label"]
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "privilegesRequired" }),
      ["searchFindings.tabSeverity.privilegesRequired.options.high.label"]
    );
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "remediationLevel" }),
      ["searchFindings.tabSeverity.remediationLevel.options.unavailable.label"]
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: "components.modal.confirm",
        })
      ).not.toBeDisabled();
    });
    await userEvent.click(
      screen.getByRole("button", {
        name: "components.modal.confirm",
      })
    );
    await waitFor(
      (): void => {
        expect(msgSuccess).toHaveBeenLastCalledWith(
          "group.findings.addModal.alerts.addedFinding",
          "groupAlerts.titleSuccess"
        );
      },
      { timeout: 2000 }
    );
  });
});
