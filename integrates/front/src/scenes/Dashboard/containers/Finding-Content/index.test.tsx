import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { GET_GROUP_SERVICES } from "hooks/queries";
import { GET_ORG_EVENTS } from "scenes/Dashboard/components/EventBar/queries";
import { FindingContent } from "scenes/Dashboard/containers/Finding-Content";
import { GET_LANGUAGE } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/queries";
import {
  GET_FINDING_HEADER,
  REMOVE_FINDING_MUTATION,
} from "scenes/Dashboard/containers/Finding-Content/queries";
import {
  GET_FINDING_INFO,
  GET_FINDING_NZR_VULNS,
  GET_FINDING_VULN_DRAFTS,
  GET_FINDING_ZR_VULNS,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_FINDINGS } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

const mockHistoryReplace: jest.Mock = jest.fn();

jest.mock(
  "react-router-dom",
  (): Record<string, unknown> => ({
    ...jest.requireActual<Record<string, unknown>>("react-router-dom"),
    useHistory: (): { replace: (path: string) => void } => ({
      replace: mockHistoryReplace,
    }),
  })
);

describe("FindingContent", (): void => {
  const btnCancel = "components.modal.cancel";
  const btnConfirm = "components.modal.confirm";

  const findingMock: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canRetrieveHacker: true,
        findingId: "438679960",
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          closedVulns: 0,
          currentState: "APPROVED",
          hacker: "machine@fluidattacks.com",
          id: "438679960",
          maxOpenSeverityScore: 3.0,
          minTimeToRemediate: 60,
          openVulns: 3,
          releaseDate: "2018-12-04 09:04:13",
          reportDate: "2017-12-04 09:04:13",
          status: "VULNERABLE",
          title: "050. Guessed weak credentials",
          totalOpenCVSSF: 0.0,
        },
      },
    },
  };

  const removeFindingMock: Readonly<MockedResponse> = {
    request: {
      query: GET_FINDING_HEADER,
      variables: {
        canRetrieveHacker: true,
        findingId: "438679960",
      },
    },
    result: {
      data: {
        finding: {
          __typename: "Finding",
          closedVulns: 0,
          currentState: "CREATED",
          hacker: "",
          id: "438679960",
          maxOpenSeverityScore: 2.9,
          minTimeToRemediate: 60,
          openVulns: 6,
          releaseDate: null,
          reportDate: "2017-12-04 09:04:13",
          status: "VULNERABLE",
          title: "050. Guessed weak credentials",
          totalOpenCVSSF: 1.308,
        },
      },
    },
  };

  const mockedVulnsQueries = [
    {
      request: {
        query: GET_FINDING_ZR_VULNS,
        variables: {
          canRetrieveZeroRisk: false,
          findingId: "438679960",
          first: 100,
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "438679960",
            zeroRiskConnection: {
              edges: [],
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
        query: GET_FINDING_INFO,
        variables: {
          findingId: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "438679960",
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
        query: GET_FINDING_NZR_VULNS,
        variables: {
          findingId: "438679960",
          first: 100,
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "438679960",
            vulnerabilitiesConnection: {
              edges: [],
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
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            businessId: "id",
            businessName: "name",
            description: "description",
            findings: [],
            hasMachine: false,
            name: "TEST",
            userRole: "user-role",
          },
        },
      },
    },
    {
      request: {
        query: GET_ORG_EVENTS,
        variables: {
          organizationName: "okada",
        },
      },
      result: {
        data: {
          organizationId: {
            __typename: "Organization",
            groups: [
              {
                __typename: "Group",
                events: [],
                name: "TEST",
              },
            ],
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: GET_FINDING_VULN_DRAFTS,
        variables: {
          canRetrieveDrafts: false,
          findingId: "438679960",
          first: 100,
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            draftsConnection: undefined,
            id: "438679960",
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
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof FindingContent).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_submit_draft_mutate" },
      { action: "api_resolvers_finding_hacker_resolve" },
    ]);

    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedVulnsQueries, findingMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "can_report_vulnerabilities" },
                  { action: "api_resolvers_finding_hacker_resolve" },
                ])
              }
            >
              <Route
                component={FindingContent}
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId"
                }
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    // Including heading inside `ContentTab`
    const numberOfHeading: number = 1;
    await waitFor((): void => {
      expect(screen.queryAllByRole("heading")).toHaveLength(numberOfHeading);
    });

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });
  });

  it("should prompt delete justification", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_resolvers_finding_hacker_resolve" },
    ]);
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedVulnsQueries, removeFindingMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "can_report_vulnerabilities" },
                  { action: "api_resolvers_finding_hacker_resolve" },
                ])
              }
            >
              <Route
                component={FindingContent}
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId"
                }
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByRole("heading", { level: 1 })).toBeInTheDocument();
    });

    expect(screen.getAllByRole("heading")[0].textContent).toContain(
      "050. Guessed weak credentials"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.btn.text")
      ).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("searchFindings.delete.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText(btnCancel)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnCancel));
    await waitFor((): void => {
      expect(screen.queryByText(btnCancel)).not.toBeInTheDocument();
    });
  });

  it("should delete finding", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const deleteMutationMock: Readonly<MockedResponse> = {
      request: {
        query: REMOVE_FINDING_MUTATION,
        variables: {
          findingId: "438679960",
          justification: "DUPLICATED",
        },
      },
      result: {
        data: {
          removeFinding: {
            success: true,
          },
        },
      },
    };

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_resolvers_finding_hacker_resolve" },
    ]);
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[
            ...mockedVulnsQueries,
            removeFindingMock,
            deleteMutationMock,
            ...mockedVulnsQueries,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "can_report_vulnerabilities" },
                  { action: "api_resolvers_finding_hacker_resolve" },
                ])
              }
            >
              <Route
                component={FindingContent}
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId"
                }
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.btn.text")
      ).not.toBeDisabled();
    });

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("searchFindings.delete.btn.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.title")
      ).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(
        screen.getByRole("combobox", { name: "justification" })
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "justification" }),
      ["DUPLICATED"]
    );

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });
  });

  it("should handle deletion errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const deleteMutationMock: Readonly<MockedResponse> = {
      request: {
        query: REMOVE_FINDING_MUTATION,
        variables: {
          findingId: "438679960",
          justification: "DUPLICATED",
        },
      },
      result: {
        errors: [new GraphQLError("Unexpected error")],
      },
    };

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_remove_finding_mutate" },
      { action: "api_resolvers_finding_hacker_resolve" },
    ]);
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/438679960/locations"]}
      >
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedVulnsQueries, removeFindingMock, deleteMutationMock]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <authzGroupContext.Provider
              value={
                new PureAbility([
                  { action: "can_report_vulnerabilities" },
                  { action: "api_resolvers_finding_hacker_resolve" },
                ])
              }
            >
              <Route
                component={FindingContent}
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId"
                }
              />
            </authzGroupContext.Provider>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.btn.text")
      ).not.toBeDisabled();
    });

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("searchFindings.delete.btn.text"));

    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.delete.title")
      ).toBeInTheDocument();
    });
    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "justification" }),
      ["DUPLICATED"]
    );

    await waitFor((): void => {
      expect(screen.queryByText(btnConfirm)).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });
  });
});
