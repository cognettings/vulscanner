import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import dayjs from "dayjs";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_FINDING_HEADER } from "../queries";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { GET_GROUP_SERVICES } from "hooks/queries";
import { VulnsView } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView";
import {
  GET_FINDING_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_VULN_DRAFTS,
  GET_FINDING_ZR_VULNS,
  RESUBMIT_VULNERABILITIES,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_GROUP_VULNERABILITIES } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { getCache } from "utils/apollo";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("VulnerabilitiesView", (): void => {
  const totalButtons = 3;
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
  const mocksGroupVulns: MockedResponse = {
    request: {
      query: GET_GROUP_VULNERABILITIES,
      variables: { first: 1200, groupName: "testgroup" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "testgroup",
          vulnerabilities: {
            edges: [],
            pageInfo: {
              endCursor: "test-cursor=",
              hasNextPage: false,
            },
          },
        },
      },
    },
  };
  const mocksQueryFindingAndGroupInfo: MockedResponse = {
    request: {
      query: GET_FINDING_INFO,
      variables: {
        findingId: "422286126",
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          id: "422286126",
          releaseDate: "2019-07-05 08:56:40",
          remediated: false,
          status: "VULNERABLE",
          totalOpenCVSSF: 0.0,
          verified: false,
        },
      },
    },
  };
  const mocksQueryFindingNzrVulns: MockedResponse = {
    request: {
      query: GET_FINDING_NZR_VULNS,
      variables: {
        findingId: "422286126",
        first: 100,
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          id: "422286126",
          vulnerabilitiesConnection: {
            edges: [
              {
                node: {
                  __typename: "Vulnerability",
                  advisories: null,
                  externalBugTrackingSystem: null,
                  findingId: "422286126",
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
                  remediated: true,
                  reportDate: dayjs().format("YYYY-MM-DD hh:mm:ss"),
                  rootNickname: "",
                  severity: "",
                  severityTemporalScore: 6.7,
                  source: "asm",
                  specific: "specific-1",
                  state: "VULNERABLE",
                  stream: "home > blog > articulo",
                  tag: "tag-1, tag-2",
                  technique: "SAST",
                  treatmentAcceptanceDate: "",
                  treatmentAcceptanceStatus: "",
                  treatmentAssigned: "assigned-user-1",
                  treatmentDate: "2019-07-05 09:56:40",
                  treatmentJustification: "test progress justification",
                  treatmentStatus: "IN_PROGRESS",
                  treatmentUser: "usertreatment@test.test",
                  verification: "Requested",
                  vulnerabilityType: "inputs",
                  where: "https://example.com/inputs",
                  zeroRisk: null,
                },
              },
              {
                node: {
                  __typename: "Vulnerability",
                  advisories: null,
                  externalBugTrackingSystem: null,
                  findingId: "422286126",
                  historicTreatment: [
                    {
                      acceptanceDate: "",
                      acceptanceStatus: "",
                      assigned: "assigned-user-4@test.test",
                      date: "2020-07-05 09:56:40",
                      justification: "test progress justification",
                      treatment: "IN PROGRESS",
                      user: "usertreatment4@test.test",
                    },
                  ],
                  id: "6903f3e4-a8ee-4a5d-ac38-fb738ec7e540",
                  lastStateDate: "2019-07-05 09:56:40",
                  lastTreatmentDate: "2019-07-05 09:56:40",
                  lastVerificationDate: null,
                  remediated: false,
                  reportDate: "2020-07-05 09:56:40",
                  rootNickname: "https:",
                  severity: "",
                  severityTemporalScore: 6.7,
                  source: "asm",
                  specific: "specific-3",
                  state: "VULNERABLE",
                  stream: null,
                  tag: "tag-3",
                  technique: "SAST",
                  treatmentAcceptanceDate: "",
                  treatmentAcceptanceStatus: "",
                  treatmentAssigned: "assigned-user-1",
                  treatmentDate: "2019-07-05 09:56:40",
                  treatmentJustification: "test progress justification",
                  treatmentStatus: "IN_PROGRESS",
                  treatmentUser: "usertreatment@test.test",
                  verification: null,
                  vulnerabilityType: "lines",
                  where: "https://example.com/tests",
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
  };
  const groupServicesQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_GROUP_SERVICES,
      variables: {
        groupName: "testgroup",
      },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "testgroup",
          serviceAttributes: [],
        },
      },
    },
  };
  const mocksQueryDraftVulns: MockedResponse = {
    request: {
      query: GET_FINDING_VULN_DRAFTS,
      variables: {
        canRetrieveDrafts: true,
        findingId: "422286126",
        first: 100,
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          draftsConnection: {
            edges: [],
            pageInfo: {
              endCursor: "test-cursor=",
              hasNextPage: false,
            },
          },
          id: "422286126",
        },
      },
    },
  };
  const mocksQueryFindingZrVulns: MockedResponse = {
    request: {
      query: GET_FINDING_ZR_VULNS,
      variables: {
        canRetrieveZeroRisk: true,
        findingId: "422286126",
        first: 100,
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          id: "422286126",
          zeroRiskConnection: {
            edges: [
              {
                node: {
                  __typename: "Vulnerability",
                  advisories: null,
                  externalBugTrackingSystem: null,
                  findingId: "422286126",
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
                  remediated: false,
                  reportDate: "2019-07-05 09:56:40",
                  rootNickname: "https:",
                  severity: "",
                  severityTemporalScore: 4.2,
                  source: "asm",
                  specific: "specific-2",
                  state: "VULNERABLE",
                  stream: null,
                  tag: "tag-3",
                  technique: "SAST",
                  treatmentAcceptanceDate: "",
                  treatmentAcceptanceStatus: "",
                  treatmentAssigned: "assigned-user-1",
                  treatmentDate: "2019-07-05 09:56:40",
                  treatmentJustification: "test progress justification",
                  treatmentStatus: "IN_PROGRESS",
                  treatmentUser: "usertreatment@test.test",
                  verification: "Verified",
                  vulnerabilityType: "lines",
                  where: "https://example.com/lines",
                  zeroRisk: "Requested",
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

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof VulnsView).toBe("function");
  });

  it("should render container", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_connection_resolve" },
      { action: "api_resolvers_finding_drafts_connection_resolve" },
    ]);

    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[
            groupServicesQuery,
            mocksQueryFindingAndGroupInfo,
            mocksQueryDraftVulns,
            mocksQueryFindingNzrVulns,
            mocksQueryFindingZrVulns,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
                }
              >
                <VulnsView refetchFindingHeader={jest.fn()} />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(totalButtons);
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
      screen.queryByText("https://example.com/inputs")
    ).toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["Verified"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("https://example.com/inputs")
      ).not.toBeInTheDocument();
    });

    expect(screen.queryByText("table.noDataIndication")).toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "verification" }),
      ["NotRequested"]
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("https://example.com/tests")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("table.noDataIndication")
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", { name: "Clear filters" })
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(totalButtons);
    });
  });

  it("should render container with additional permissions", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_confirm_vulnerabilities_zero_risk_mutate" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_connection_resolve" },
      { action: "api_resolvers_finding_drafts_connection_resolve" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[
            groupServicesQuery,
            mocksQueryFindingAndGroupInfo,
            mocksQueryDraftVulns,
            mocksQueryFindingNzrVulns,
            mocksQueryFindingZrVulns,
          ]}
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
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
                }
              >
                <VulnsView refetchFindingHeader={jest.fn()} />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(2);
    });

    expect(
      screen.queryByRole("combobox", { name: "treatment" })
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabVuln.buttons.handleAcceptance",
      })
    );
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.tabDescription.handleAcceptanceModal.title"
        )
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("combobox", { name: "treatment" })
    ).toBeInTheDocument();
  });

  it("should render container and test request_button flow", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_finding_drafts_connection_resolve" },
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_mutations_request_vulnerabilities_verification_mutate" },
      { action: "api_resolvers_finding_zero_risk_connection_resolve" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const mockedServices = new PureAbility<string>([
      { action: "is_continuous" },
      { action: "can_report_vulnerabilities" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[
            groupServicesQuery,
            mocksQueryFindingAndGroupInfo,
            mocksQueryDraftVulns,
            mocksQueryFindingNzrVulns,
            mocksQueryFindingZrVulns,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider value={mockedServices}>
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
                }
              >
                <VulnsView refetchFindingHeader={jest.fn()} />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(totalButtons);
    });

    await userEvent.click(
      screen.getByRole("checkbox", { name: "https://example.com/tests" })
    );

    expect(
      screen.queryByText(
        "searchFindings.tabDescription.remediationModal.titleRequest"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByRole("button", {
        name: "searchFindings.tabDescription.requestVerify.text",
      })
    );

    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabDescription.remediationModal.titleRequest"
        )
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).not.toBeInTheDocument();
  });

  it("should render container and test verify_button flow", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_connection_resolve" },
      { action: "api_mutations_verify_vulnerabilities_request_mutate" },
      { action: "api_resolvers_finding_drafts_connection_resolve" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[
            groupServicesQuery,
            mocksQueryFindingAndGroupInfo,
            mocksQueryDraftVulns,
            mocksQueryFindingNzrVulns,
            mocksQueryFindingZrVulns,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
                }
              >
                <VulnsView refetchFindingHeader={jest.fn()} />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(totalButtons);
    });

    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();
    expect(
      screen.getByRole("checkbox", { name: "https://example.com/tests" })
    ).not.toBeDisabled();
    expect(
      screen.queryByText(
        "searchFindings.tabDescription.remediationModal.titleObservations"
      )
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.markVerified.text")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("checkbox", { name: "https://example.com/tests" })
      ).toBeDisabled();
    });

    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).not.toBeInTheDocument();

    expect(screen.getByText("New")).toBeInTheDocument();

    expect(
      screen.getByRole("checkbox", { name: "https://example.com/inputs New" })
    ).not.toBeDisabled();

    await userEvent.click(
      screen.getByRole("checkbox", { name: "https://example.com/inputs New" })
    );
    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.markVerified.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText(
          "searchFindings.tabDescription.remediationModal.titleObservations"
        )
      ).toBeInTheDocument();
    });
  });

  it("should resubmit vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksQueryResubmitVulns: MockedResponse = {
      request: {
        query: GET_FINDING_VULN_DRAFTS,
        variables: {
          canRetrieveDrafts: true,
          findingId: "422286126",
          first: 100,
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            draftsConnection: {
              edges: [
                {
                  node: {
                    __typename: "Vulnerability",
                    advisories: null,
                    externalBugTrackingSystem: null,
                    findingId: "422286126",
                    historicTreatment: [],
                    id: "6b855957-9b94-485f-ad43-82b5f184e826",
                    lastStateDate: "2019-07-05 09:56:40",
                    lastTreatmentDate: "2019-07-05 09:56:40",
                    lastVerificationDate: null,
                    remediated: true,
                    reportDate: dayjs().format("YYYY-MM-DD hh:mm:ss"),
                    rootNickname: "",
                    severity: "",
                    severityTemporalScore: 6.7,
                    source: "asm",
                    specific: "specific-4",
                    state: "REJECTED",
                    stream: "home > blog > articulo",
                    tag: "tag-1, tag-2",
                    technique: "DAST",
                    treatmentAcceptanceDate: "",
                    treatmentAcceptanceStatus: "",
                    treatmentAssigned: "assigned-user-1",
                    treatmentDate: "2019-07-05 09:56:40",
                    treatmentJustification: "test progress justification",
                    treatmentStatus: "IN_PROGRESS",
                    treatmentUser: "usertreatment@test.test",
                    verification: null,
                    vulnerabilityType: "inputs",
                    where: "https://example.com/inputs-4",
                    zeroRisk: null,
                  },
                },
                {
                  node: {
                    __typename: "Vulnerability",
                    advisories: null,
                    externalBugTrackingSystem: null,
                    findingId: "422286126",
                    historicTreatment: [],
                    id: "6a9904a0-7c83-4444-8bf9-61b53b865129",
                    lastStateDate: "2019-07-05 09:56:40",
                    lastTreatmentDate: "2019-07-05 09:56:40",
                    lastVerificationDate: null,
                    remediated: false,
                    reportDate: "2020-07-05 09:56:40",
                    rootNickname: "https:",
                    severity: "",
                    severityTemporalScore: 6.7,
                    source: "asm",
                    specific: "specific-5",
                    state: "SUBMITTED",
                    stream: null,
                    tag: "tag-3",
                    technique: "DAST",
                    treatmentAcceptanceDate: "",
                    treatmentAcceptanceStatus: "",
                    treatmentAssigned: "assigned-user-1",
                    treatmentDate: "2019-07-05 09:56:40",
                    treatmentJustification: "test progress justification",
                    treatmentStatus: "IN_PROGRESS",
                    treatmentUser: "usertreatment@test.test",
                    verification: null,
                    vulnerabilityType: "inputs",
                    where: "https://example.com/tests-5",
                    zeroRisk: null,
                  },
                },
              ],
              pageInfo: {
                endCursor: "test-cursor=",
                hasNextPage: false,
              },
            },
            id: "422286126",
          },
        },
      },
    };
    const mockedMutation: MockedResponse = {
      request: {
        query: RESUBMIT_VULNERABILITIES,
        variables: {
          findingId: "422286126",
          vulnerabilities: ["6b855957-9b94-485f-ad43-82b5f184e826"],
        },
      },
      result: {
        data: { resubmitVulnerabilities: { success: true } },
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_vulnerability_hacker_resolve" },
      { action: "api_resolvers_finding_zero_risk_connection_resolve" },
      { action: "api_resolvers_finding_drafts_connection_resolve" },
      { action: "api_mutations_resubmit_vulnerabilities_mutate" },
    ]);

    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/testorg/groups/testgroup/vulns/422286126/locations",
        ]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[
            groupServicesQuery,
            mockedMutation,
            mocksQueryFindingAndGroupInfo,
            mocksQueryResubmitVulns,
            mocksQueryFindingNzrVulns,
            mocksQueryFindingZrVulns,
            mocksQueryFindingAndGroupInfo,
            mocksFindingHeader,
            mocksQueryFindingNzrVulns,
            mocksQueryFindingZrVulns,
            mocksQueryResubmitVulns,
            mocksGroupVulns,
            mocksFindingHeader,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([{ action: "can_report_vulnerabilities" }])
              }
            >
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId/locations"
                }
              >
                <VulnsView refetchFindingHeader={jest.fn()} />
              </Route>
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: /searchfindings\.tabvuln\.buttons\.resubmit/iu,
        })
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("checkbox", {
        name: /https:\/\/example\.com\/inputs new/iu,
      })
    );
    await userEvent.click(
      screen.getByRole("checkbox", {
        name: /https:\/\/example\.com\/inputs-4/iu,
      })
    );

    expect(
      screen.getByRole("checkbox", {
        name: /https:\/\/example\.com\/inputs new/iu,
      })
    ).toBeEnabled();
    expect(
      screen.getByRole("checkbox", {
        name: /https:\/\/example\.com\/inputs-4/iu,
      })
    ).toBeEnabled();

    await userEvent.click(
      screen.getByRole("button", {
        name: /searchfindings\.tabvuln\.buttons\.resubmit/iu,
      })
    );
    await userEvent.click(
      screen.getByRole("button", {
        name: /searchfindings\.tabvuln\.buttons\.resubmit/iu,
      })
    );

    expect(msgSuccess).toHaveBeenCalledWith(
      "Vulnerability has been submitted",
      "Correct!"
    );
  });
});
