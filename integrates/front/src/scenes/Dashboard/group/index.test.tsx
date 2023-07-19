import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GROUP_EVENT_STATUS } from "./queries";

import { GroupContent } from ".";
import { GET_ORG_EVENTS } from "../components/EventBar/queries";
import { GET_LANGUAGE } from "../containers/Finding-Content/DescriptionView/queries";
import {
  GET_FINDINGS,
  GET_ROOTS,
} from "../containers/Group-Content/GroupFindingsView/queries";
import { GET_GROUP_DATA } from "../containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import type { IGroupData } from "../containers/Group-Content/GroupScopeView/GroupSettingsView/Services/types";
import type { IGetOrganizationId } from "../containers/Organization-Content/OrganizationNav/types";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { GET_GROUP_SERVICES } from "hooks/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { getCache } from "utils/apollo";

describe("groupContent", (): void => {
  const groupMock: MockedResponse<IGroupData> = {
    request: {
      query: GET_GROUP_DATA,
      variables: {
        groupName: "testgroup",
      },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          businessId: "",
          businessName: "",
          description: "",
          hasForces: true,
          hasMachine: true,
          hasSquad: false,
          language: "",
          managed: "UNDER_REVIEW",
          name: "testgroup",
          organization: { name: "testorg" },
          service: "",
          sprintDuration: "",
          sprintStartDate: "",
          subscription: "",
        },
      },
    },
  };

  const groupFindingsMock = {
    group: {
      __typename: "Group",
      businessId: "id",
      businessName: "name",
      description: "description",
      findings: [],
      hasMachine: false,
      name: "testgroup",
      userRole: "user-role",
    },
  };

  const findingMock: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          groupName: "testgroup",
        },
      },
      result: {
        data: groupFindingsMock,
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: "" },
          groupName: "testgroup",
        },
      },
      result: {
        data: groupFindingsMock,
      },
    },
    {
      request: {
        query: GET_FINDINGS,
        variables: {
          canGetRejectedVulnerabilities: false,
          canGetSubmittedVulnerabilities: false,
          filters: { root: undefined },
          groupName: "testgroup",
        },
      },
      result: {
        data: groupFindingsMock,
      },
    },
  ];
  const languageQuery: Readonly<MockedResponse> = {
    request: {
      query: GET_LANGUAGE,
      variables: { groupName: "testgroup" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          language: "EN",
          name: "testgroup",
        },
      },
    },
  };
  const servicesQuery: MockedResponse = {
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

  const rootsQuery: MockedResponse = {
    request: {
      query: GET_ROOTS,
      variables: {
        groupName: "testgroup",
      },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "testgroup",
          roots: [],
        },
      },
    },
  };
  const orgEventsQuery: MockedResponse = {
    request: {
      query: GET_ORG_EVENTS,
      variables: {
        organizationName: "testorg",
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
              name: "testgroup",
            },
          ],
          name: "testorg",
        },
      },
    },
  };
  const groupEventsQuery: MockedResponse = {
    request: {
      query: GET_GROUP_EVENT_STATUS,
      variables: {
        groupName: "testgroup",
      },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          events: [],
          name: "testgroup",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupContent).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_ID,
          variables: {
            organizationName: "testorg",
          },
        },
        result: {
          data: {
            organizationId: {
              __typename: "Organization",
              id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
              name: "testorg",
            },
          },
        },
      },
      ...findingMock,
      groupEventsQuery,
      groupMock,
      languageQuery,
      orgEventsQuery,
      rootsQuery,
      servicesQuery,
    ];
    const numberOfLinksWithPermissions: number = 7;
    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_group_consulting_resolve" },
      { action: "api_resolvers_query_stakeholder__resolve_for_group" },
      { action: "api_resolvers_group_drafts_resolve" },
      { action: "api_resolvers_group_billing_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider cache={getCache()} mocks={mockedQueries}>
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_squad" }])}
          >
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <Route path={"/orgs/:organizationName/groups/:groupName/vulns"}>
                <GroupContent />
              </Route>
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(
        numberOfLinksWithPermissions
      );
    });
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    jest.spyOn(console, "error").mockImplementation();
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_ID,
          variables: {
            organizationName: "testorg",
          },
        },
        result: {
          data: {
            organizationId: {
              __typename: "Organization",
              id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
              name: "testorg",
            },
          },
        },
      },
      ...findingMock,
      groupEventsQuery,
      groupMock,
      languageQuery,
      orgEventsQuery,
      rootsQuery,
      servicesQuery,
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider cache={getCache()} mocks={mockedQueries}>
          <authzPermissionsContext.Provider value={new PureAbility([])}>
            <Route path={"/orgs/:organizationName/groups/:groupName/vulns"}>
              <GroupContent />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(5);
    });
  });

  it("should prevent access under review", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const orgMock: MockedResponse<IGetOrganizationId> = {
      request: {
        query: GET_ORGANIZATION_ID,
        variables: {
          organizationName: "testorg",
        },
      },
      result: {
        data: {
          organizationId: {
            __typename: "Organization",
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "testorg",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            orgMock,
            ...findingMock,
            groupEventsQuery,
            groupMock,
            languageQuery,
            orgEventsQuery,
            rootsQuery,
            servicesQuery,
          ]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_squad" }])}
          >
            <authzPermissionsContext.Provider value={new PureAbility([])}>
              <Route path={"/orgs/:organizationName/groups/:groupName/vulns"}>
                <GroupContent />
              </Route>
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.accessDenied.title")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("group.accessDenied.btn")
    ).not.toBeInTheDocument();
  });

  it("should allow dismissing", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const orgMock: MockedResponse<IGetOrganizationId> = {
      request: {
        query: GET_ORGANIZATION_ID,
        variables: {
          organizationName: "testorg",
        },
      },
      result: {
        data: {
          organizationId: {
            __typename: "Organization",
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "testorg",
          },
        },
      },
    };

    render(
      <MemoryRouter initialEntries={["/orgs/testorg/groups/testgroup/vulns"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            orgMock,
            ...findingMock,
            groupEventsQuery,
            ...findingMock,
            groupMock,
            languageQuery,
            orgEventsQuery,
            rootsQuery,
            servicesQuery,
            languageQuery,
          ]}
        >
          <authzGroupContext.Provider
            value={new PureAbility([{ action: "has_squad" }])}
          >
            <authzPermissionsContext.Provider
              value={
                new PureAbility([
                  { action: "api_mutations_update_group_managed_mutate" },
                ])
              }
            >
              <Route path={"/orgs/:organizationName/groups/:groupName/vulns"}>
                <GroupContent />
              </Route>
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryByText("group.accessDenied.btn")).toBeInTheDocument();
    });

    expect(
      screen.queryByText("group.tabs.findings.text")
    ).not.toBeInTheDocument();

    // Expect(continueAccess).toBeInTheDocument();

    // await act(async () => {

    await userEvent.click(screen.getByText("group.accessDenied.btn"));

    await waitFor((): void => {
      expect(
        screen.queryByText("group.tabs.findings.text")
      ).toBeInTheDocument();
    });
    // });
  });
});
