import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GROUP_DATA } from "../GroupScopeView/GroupSettingsView/queries";
import { authzPermissionsContext } from "context/authz/config";
import { GET_ORG_EVENTS } from "scenes/Dashboard/components/EventBar/queries";
import { GET_GROUP_CONSULTING } from "scenes/Dashboard/containers/Group-Content/GroupConsultingView/queries";
import { GroupRoute } from "scenes/Dashboard/containers/Group-Content/GroupRoute";
import { GET_GROUP_DATA as GET_GROUP_DATA_ROUTE } from "scenes/Dashboard/containers/Group-Content/GroupRoute/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { GET_GROUP_EVENT_STATUS } from "scenes/Dashboard/group/queries";
import { GET_GROUP_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import { getCache } from "utils/apollo";
import { msgError } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("groupRoute", (): void => {
  const baseMockedQueries: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_LEVEL_PERMISSIONS,
        variables: {
          identifier: "test",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "test",
            permissions: ["api_resolvers_group_consulting_resolve"],
            userRole: "user",
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
            __typename: "Organization",
            id: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_EVENT_STATUS,
        variables: {
          groupName: "test",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            events: [],
            name: "test",
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
            __typename: "Group",
            groups: [
              {
                __typename: "Group",
                events: [],
                name: "test",
              },
            ],
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "test",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            businessId: "",
            businessName: "",
            description: "Integrates unit test project",
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            managed: "MANAGED",
            name: "test",
            service: "WHITE",
            sprintDuration: "1",
            sprintStartDate: "",
            subscription: "CoNtInUoUs",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_CONSULTING,
        variables: { groupName: "test" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            consulting: [],
            name: "test",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupRoute).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_DATA_ROUTE,
          variables: {
            groupName: "test",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              name: "test",
              organization: "okada",
              serviceAttributes: ["has_asm"],
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_group_consulting_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/test/consulting"]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MockedProvider
            cache={getCache()}
            mocks={[
              ...baseMockedQueries,
              ...mockedQueries,
              ...baseMockedQueries,
              ...mockedQueries,
            ]}
          >
            <Route path={"/orgs/:organizationName/groups/:groupName"}>
              <GroupRoute />
            </Route>
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </MemoryRouter>
    );
    const numberOfTabs: number = 5;

    await expect(screen.findAllByRole("listitem")).resolves.toHaveLength(
      numberOfTabs
    );

    jest.clearAllMocks();
  });

  it("should render error in component", async (): Promise<void> => {
    expect.hasAssertions();

    const mockError: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_DATA_ROUTE,
          variables: {
            groupName: "test",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/test"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockError, ...baseMockedQueries]}
        >
          <Route path={"/orgs/:organizationName/groups/:groupName"}>
            <GroupRoute />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });
});
