/* eslint-disable camelcase */
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { REMOVE_VULN_MUTATION } from "scenes/Dashboard/components/RemoveVulnerability/queries";
import { GET_FINDING_HEADER } from "scenes/Dashboard/containers/Finding-Content/queries";
import { GET_FINDING_INFO } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GroupVulnerabilitiesView } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView";
import {
  GET_GROUP_VULNERABILITIES,
  GET_GROUP_VULNERABILITY_DRAFTS,
} from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities/queries";
import { getCache } from "utils/apollo";

const mockedFetch: FetchMockStatic = fetch as FetchMockStatic & typeof fetch;
const baseUrl: string =
  "https://gitlab.com/api/v4/projects/20741933/repository/files";
const branchRef: string = "trunk";
const vulnsFileId: string =
  "common%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`, {
  body: {
    "038": {
      en: {
        description: "",
        impact: "",
        recommendation: "",
        threat: "",
        title: "Business information leak",
      },
      requirements: [],
      score: {
        base: {
          attack_complexity: "",
          attack_vector: "",
          availability: "",
          confidentiality: "",
          integrity: "",
          privileges_required: "",
          scope: "",
          user_interaction: "",
        },
        temporal: {
          exploit_code_maturity: "",
          remediation_level: "",
          report_confidence: "",
        },
      },
    },
  },

  status: 200,
});
const requirementsFileId: string =
  "common%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
mockedFetch.mock(`${baseUrl}/${requirementsFileId}/raw?ref=${branchRef}`, {
  body: {
    "176": {
      category: "",
      en: {
        description: "",
        summary: `
          The system must restrict access
          to system objects
          that have sensitive content.
          It should only allow access
          to authorized users.
        `,
        title: "Restrict system objects",
      },
      references: [],
    },
    "177": {
      category: "",
      en: {
        description: "",
        summary: `
          The system must not store
          sensitive information
          in temporary files or cache memory.
        `,
        title: "Avoid caching and temporary files",
      },
      references: [],
    },
  },

  status: 200,
});

describe("GroupVulnerabilitiesView", (): void => {
  const mockGroupVulnerabilities = {
    group: {
      __typename: "Group",
      name: "unittesting",
      vulnerabilities: {
        edges: [
          {
            node: {
              __typename: "Vulnerability",
              assigned: "",
              externalBugTrackingSystem: null,
              finding: {
                id: "438679960",
                title: "038. Business information leak",
              },
              findingId: "438679960",
              groupName: "unittesting",
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
              organizationName: "test",
              remediated: false,
              reportDate: "2019-05-23 21:19:29",
              rootNickname: "https:",
              severity: "2.7",
              severityTemporalScore: 2.7,
              source: "asm",
              specific: "specific-1",
              state: "VULNERABLE",
              stream: null,
              tag: "tag-1, tag-2",
              technique: "SAST",
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
          },
          {
            node: {
              __typename: "Vulnerability",
              assigned: "",
              externalBugTrackingSystem: null,
              finding: {
                id: "438679960",
                title: "038. Business information leak",
              },
              findingId: "438679960",
              groupName: "unittesting",
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
              lastVerificationDate: null,
              organizationName: "test",
              remediated: false,
              reportDate: "",
              rootNickname: "https:",
              severity: "1",
              severityTemporalScore: 1.0,
              source: "asm",
              specific: "specific-2",
              state: "SAFE",
              stream: null,
              tag: "tag-3, tag-4",
              technique: "SAST",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-2",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentStatus: "",
              treatmentUser: "usertreatment@test.test",
              verification: "Verified",
              vulnerabilityType: "lines",
              where: "https://example.com/lines",
              zeroRisk: null,
            },
          },
          {
            node: {
              __typename: "Vulnerability",
              assigned: "",
              externalBugTrackingSystem: null,
              finding: {
                id: "438679960",
                title: "038. Business information leak",
              },
              findingId: "438679960",
              groupName: "unittesting",
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
              lastVerificationDate: "2019-07-05 09:56:40",
              organizationName: "test",
              remediated: false,
              reportDate: "",
              rootNickname: "https:",
              severity: "1",
              severityTemporalScore: 1.0,
              source: "asm",
              specific: "specific-3",
              state: "VULNERABLE",
              stream: null,
              tag: "tag-5, tag-6",
              technique: "SAST",
              treatmentAcceptanceDate: "",
              treatmentAcceptanceStatus: "",
              treatmentAssigned: "assigned-user-3",
              treatmentDate: "2019-07-05 09:56:40",
              treatmentJustification: "test progress justification",
              treatmentStatus: "IN_PROGRESS",
              treatmentUser: "usertreatment@test.test",
              verification: "Verified",
              vulnerabilityType: "lines",
              where: "https://example.com/lines",
              zeroRisk: null,
            },
          },
        ],
        pageInfo: {
          endCursor: "bnVsbA==",
          hasNextPage: false,
        },
        total: 3,
      },
    },
  };

  const mockedPermissions = new PureAbility<string>([
    { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_handle_vulnerabilities_acceptance_mutate" },
    { action: "api_mutations_reject_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_remove_vulnerability_tags_mutate" },
    { action: "api_mutations_request_vulnerabilities_verification_mutate" },
    { action: "api_mutations_request_vulnerabilities_zero_risk_mutate" },
    { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    { action: "api_mutations_verify_vulnerabilities_request_mutate" },
    { action: "can_assign_vulnerabilities_to_fluidattacks_staff" },
    { action: "api_resolvers_group_vulnerability_drafts_resolve" },
    { action: "api_mutations_remove_vulnerability_mutate" },
  ]);

  const queryMock: readonly MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 150,
          groupName: "unittesting",
          search: "",
        },
      },
      result: {
        data: mockGroupVulnerabilities,
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 150,
          groupName: "unittesting",
          root: "",
          search: "",
          stateStatus: "",
          treatment: "",
          type: "",
          verificationStatus: "On_hold",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            vulnerabilities: {
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
              total: 0,
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 150,
          groupName: "unittesting",
          root: "",
          search: "",
          stateStatus: "",
          treatment: "",
          type: "",
          verificationStatus: "Requested",
        },
      },
      result: {
        data: mockGroupVulnerabilities,
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 150,
          groupName: "unittesting",
          root: "",
          search: "",
          stateStatus: "",
          treatment: "",
          type: "",
          verificationStatus: "NotRequested",
        },
      },
      result: {
        data: mockGroupVulnerabilities,
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 150,
          groupName: "unittesting",
          root: "",
          search: "",
          stateStatus: "",
          treatment: "",
          type: "",
          verificationStatus: "Verified",
        },
      },
      result: {
        data: mockGroupVulnerabilities,
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITIES,
        variables: {
          first: 100,
          groupName: "unittesting",
          zeroRisk: "REQUESTED",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            vulnerabilities: {
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
              total: 0,
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITY_DRAFTS,
        variables: {
          canRetrieveDrafts: true,
          first: 150,
          groupName: "unittesting",
          search: "",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            vulnerabilityDrafts: {
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
              total: 0,
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITY_DRAFTS,
        variables: {
          canRetrieveDrafts: true,
          first: 150,
          groupName: "unittesting",
          root: undefined,
          search: undefined,
          stateStatus: undefined,
          type: undefined,
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            vulnerabilityDrafts: {
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
              total: 0,
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITY_DRAFTS,
        variables: {
          canRetrieveDrafts: true,
          first: 150,
          groupName: "unittesting",
          root: "",
          search: undefined,
          stateStatus: "",
          type: "",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            vulnerabilityDrafts: {
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
              total: 0,
            },
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_VULNERABILITY_DRAFTS,
        variables: {
          canRetrieveDrafts: true,
          first: 150,
          groupName: "unittesting",
          root: "",
          search: undefined,
          stateStatus: "",
          type: "",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            vulnerabilityDrafts: {
              edges: [],
              pageInfo: {
                endCursor: "bnVsbA==",
                hasNextPage: false,
              },
              total: 0,
            },
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupVulnerabilitiesView).toBe("function");
  });

  it("should render in group vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider cache={getCache()} mocks={queryMock}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should display all group vulnerabilities columns", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider cache={getCache()} mocks={queryMock}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getByText("Vulnerability")).toBeInTheDocument();
    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Criteria")).toBeInTheDocument();
    expect(screen.getByText("Found")).toBeInTheDocument();
    expect(screen.getByText("Severity")).toBeInTheDocument();
    expect(screen.getByText("Evidence")).toBeInTheDocument();

    expect(
      screen.getByText("https://example.com/inputs | specific-1")
    ).toBeInTheDocument();
    expect(screen.getAllByText("038. business information leak")).toHaveLength(
      3
    );
    expect(screen.getAllByText("Vulnerable")[0]).toBeInTheDocument();
    expect(screen.getByText("In progress")).toBeInTheDocument();
    expect(screen.getByText("Requested")).toBeInTheDocument();
    expect(screen.getAllByText("Code")[0]).toBeInTheDocument();
    expect(screen.getByText("2019-05-23")).toBeInTheDocument();
    expect(screen.getByText("2.7")).toBeInTheDocument();
    expect(screen.getAllByText("View")[0]).toBeInTheDocument();

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should have Filter button", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider cache={getCache()} mocks={queryMock}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should have Filter options", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider
            cache={getCache()}
            mocks={[...queryMock, ...queryMock, ...queryMock, ...queryMock]}
          >
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );
    await userEvent.click(screen.getByText("Add filter"));

    expect(screen.getByText("Root")).toBeInTheDocument();
    expect(screen.getByText("Source")).toBeInTheDocument();
    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Treatment")).toBeInTheDocument();
    expect(screen.getByText("Reattack")).toBeInTheDocument();

    await userEvent.click(screen.getAllByText("Status")[1]);

    expect(
      screen.getByRole("option", {
        name: "Vulnerable",
      })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("option", {
        name: "Safe",
      })
    ).toBeInTheDocument();

    await userEvent.click(screen.getAllByText("Treatment")[1]);

    await waitFor((): void => {
      expect(screen.getAllByText("In progress")[1]).toBeInTheDocument();
    });

    expect(screen.getByText("Untreated")).toBeInTheDocument();
    expect(screen.getByText("Temporarily accepted")).toBeInTheDocument();
    expect(screen.getByText("Permanently accepted")).toBeInTheDocument();

    await userEvent.click(screen.getAllByText("Reattack")[1]);

    await waitFor((): void => {
      expect(screen.getAllByText("Requested")[1]).toBeInTheDocument();
    });

    expect(screen.queryByText("Not requested")).toBeInTheDocument();
    expect(screen.getByText("On hold")).toBeInTheDocument();
    expect(screen.getByText("Verified")).toBeInTheDocument();

    await userEvent.click(screen.getAllByText("Source")[1]);

    await waitFor((): void => {
      expect(screen.getByText("app")).toBeInTheDocument();
    });

    expect(screen.getByText("infra")).toBeInTheDocument();
    expect(screen.getByText("code")).toBeInTheDocument();

    expect(screen.getByRole("textbox", { name: "root" })).toBeInTheDocument();

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    expect(
      screen.getByRole("button", { name: "Clear filters" })
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["On_hold"]
    );
    await waitFor((): void => {
      expect(screen.queryByText("table.noDataIndication")).toBeInTheDocument();
    });

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["Requested"]
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("table.noDataIndication")
      ).not.toBeInTheDocument();
    });

    expect(
      screen.queryByText("https://example.com/inputs | specific-1")
    ).toBeInTheDocument();
    expect(screen.queryAllByRole("row")).toHaveLength(2);

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["NotRequested"]
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("https://example.com/lines | specific-3")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("table.noDataIndication")
    ).not.toBeInTheDocument();
    expect(screen.queryAllByRole("row")).toHaveLength(2);

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["Verified"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("https://example.com/inputs | specific-1")
      ).not.toBeInTheDocument();
    });

    expect(screen.queryAllByRole("row")).toHaveLength(3);

    expect(
      screen.queryByText("table.noDataIndication")
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("https://example.com/lines | specific-3")
    ).toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["All"]
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should open verify vulnerabilities modal", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={[...queryMock, ...queryMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <Route
                component={GroupVulnerabilitiesView}
                path={"/groups/:groupName/vulns"}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabDescription.markVerified.text",
      })
    );

    await waitFor((): void => {
      expect(screen.getByText("Where")).toBeInTheDocument();
    });

    expect(screen.getByText("Specific")).toBeInTheDocument();
    expect(screen.getByText("State")).toBeInTheDocument();
    expect(screen.getByText("specific-1")).toBeInTheDocument();

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should open treatment acceptance modal", async (): Promise<void> => {
    expect.hasAssertions();

    const queryZeroRiskMock: readonly MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_VULNERABILITIES,
          variables: {
            first: 100,
            groupName: "unittesting",
            zeroRisk: "REQUESTED",
          },
        },
        result: {
          data: {
            group: {
              name: "unittesting",
              vulnerabilities: {
                edges: [
                  {
                    node: {
                      assigned: "",
                      externalBugTrackingSystem: null,
                      finding: {
                        id: "438679961",
                        title: "002. Test draft title",
                      },
                      findingId: "438679961",
                      groupName: "unittesting",
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
                      id: "89521e9a-b1a3-4047-a16e-15d530dc1341",
                      lastStateDate: "2019-07-05 09:56:40",
                      lastTreatmentDate: "2019-07-05 09:56:40",
                      lastVerificationDate: null,
                      organizationName: "test",
                      remediated: false,
                      reportDate: "2019-05-23 21:19:29",
                      rootNickname: "https:",
                      severity: "2.7",
                      severityTemporalScore: 7.2,
                      source: "asm",
                      specific: "specific-4",
                      state: "VULNERABLE",
                      stream: null,
                      tag: "tag-1, tag-2",
                      treatmentAcceptanceDate: "",
                      treatmentAcceptanceStatus: "",
                      treatmentAssigned: "assigned-user-4",
                      treatmentDate: "2019-07-05 09:56:40",
                      treatmentJustification: "test progress justification",
                      treatmentStatus: "",
                      treatmentUser: "usertreatment@test.test",
                      verification: "Requested",
                      vulnerabilityType: "inputs",
                      where: "https://example.com/inputs2",
                      zeroRisk: "Requested",
                    },
                  },
                ],
              },
            },
          },
        },
      },
      ...queryMock,
    ];

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...queryZeroRiskMock, ...queryMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={new PureAbility([{ action: "can_request_zero_risk" }])}
            >
              <Route
                component={GroupVulnerabilitiesView}
                path={"/groups/:groupName/vulns"}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabVuln.buttons.handleAcceptance",
      })
    );

    expect(screen.getByText("Where")).toBeInTheDocument();
    expect(screen.getByText("Specific")).toBeInTheDocument();
    expect(screen.getByText("Acceptance")).toBeInTheDocument();

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should open reattack modal", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={[...queryMock, ...queryMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "is_continuous" },
                  { action: "can_report_vulnerabilities" },
                ])
              }
            >
              <Route
                component={GroupVulnerabilitiesView}
                path={"/groups/:groupName/vulns"}
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabDescription.requestVerify.text",
      })
    );

    expect(
      screen.getByText("searchFindings.tabDescription.remediationModal.message")
    ).toBeInTheDocument();

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should open edit modal", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={[...queryMock, ...queryMock]}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });
    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabVuln.buttons.edit",
      })
    );

    expect(
      screen.getByText("searchFindings.tabDescription.editVuln")
    ).toBeInTheDocument();

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("treatment cell should have format", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getByText("In progress")).toBeInTheDocument();
    expect(screen.getByText("In progress")).toHaveStyle(
      `background-color: #ffeecc;
      border: 1px solid #d88218;
      color: #d88218;`
    );

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("source cell should have format", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getAllByText("Code")[0]).toBeInTheDocument();
    expect(screen.getAllByText("Code")[0]).toHaveStyle(
      `background-color: #dce4f7;
      border: 1px solid #3778ff;
      color: #3778ff;`
    );

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("reattack cell should have format", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getByText("Requested")).toBeInTheDocument();
    expect(screen.getByText("Requested")).toHaveStyle(
      `background-color: #ffeecc;
      border: 1px solid #d88218;
      color: #d88218;`
    );

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("should not have gray color in format", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider cache={getCache()} mocks={queryMock}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupVulnerabilitiesView}
              path={"/groups/:groupName/vulns"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.queryAllByText("Code")[0]).not.toHaveStyle(
      `background-color: #d2d2da;
      border: 1px solid #2e2e38;
      color: #2e2e38;`
    );
    expect(screen.queryByText("In progress")).not.toHaveStyle(
      `background-color: #d2d2da;
      border: 1px solid #2e2e38;
      color: #2e2e38;`
    );
    expect(screen.queryAllByText("Vulnerable")[0]).not.toHaveStyle(
      `background-color: #d2d2da;
      border: 1px solid #2e2e38;
      color: #2e2e38;`
    );
    expect(screen.queryByText("Safe")).not.toHaveStyle(
      `background-color: #d2d2da;
      border: 1px solid #2e2e38;
      color: #2e2e38;`
    );

    sessionStorage.clear();
    jest.clearAllMocks();
  });

  it("remove and refetch", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: readonly MockedResponse[] = [
      {
        request: {
          query: REMOVE_VULN_MUTATION,
          variables: {
            findingId: "438679960",
            id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
            justification: "DUPLICATED",
          },
        },
        result: {
          data: {
            removeVulnerability: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_FINDING_HEADER,
          variables: {
            canRetrieveHacker: false,
            findingId: "438679960",
          },
        },
        result: {
          data: {
            finding: {
              closedVulns: 0,
              currentState: "APPROVED",
              id: "438679960",
              maxOpenSeverityScore: 0.0,
              minTimeToRemediate: 60,
              openVulns: 0,
              releaseDate: "2019-05-08",
              reportDate: "2019-04-08",
              status: "SAFE",
              title: "038. Business information leak",
              totalOpenCVSSF: 0.0,
            },
          },
        },
      },
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              userEmail: "test@test.test",
              vulnerabilitiesAssigned: [],
            },
          },
        },
      },
      {
        request: {
          query: GET_FINDING_INFO,
          variables: {
            findingId: "438679960",
          },
        },
        result: {
          data: {
            finding: {
              id: "438679960",
              releaseDate: "2019-05-08",
              remediated: false,
              status: "false",
              totalOpenCVSSF: 0.0,
              verified: false,
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
              userEmail: "test@test.test",
              vulnerabilitiesAssigned: [],
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/vulns"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...queryMock, ...mocksMutation, ...queryMock]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route
                component={GroupVulnerabilitiesView}
                path={"/groups/:groupName/vulns"}
              />
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
    });

    expect(screen.getAllByRole("row")).toHaveLength(4);
    expect(screen.queryByText("deleteVulns.title")).not.toBeInTheDocument();

    await userEvent.click(
      screen.getAllByRole("button", { name: "remove-row" })[0]
    );

    await waitFor((): void => {
      expect(screen.queryByText("deleteVulns.title")).toBeInTheDocument();
    });

    await userEvent.selectOptions(screen.getByRole("combobox"), ["DUPLICATED"]);

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(3);
    });

    sessionStorage.clear();
    jest.clearAllMocks();
  });
});
