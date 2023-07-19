import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "./to-do/queries";
import { GET_USER_ROLE } from "./user-profile/role/queries";

import { Navbar } from ".";
import { authContext } from "context/auth";
import { authzPermissionsContext } from "context/authz/config";
import { GET_GROUP_SERVICES } from "hooks/queries";
import {
  GET_FINDING_TITLE,
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "pages/home/dashboard/navbar/breadcrumb/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import { getCache } from "utils/apollo";

const mockHistoryPush = jest.fn();
jest.mock("react-router-dom", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("navbar", (): void => {
  const mockedOrganizationGroup: MockedResponse[] = [
    {
      request: {
        query: GET_USER_ROLE,
        variables: {
          groupLevel: true,
          groupName: "unittesting",
          organizationLevel: false,
          organizationName: "okada",
          userLevel: false,
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            userRole: "user",
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
                __typename: "Group",
                name: "group1",
              },
              {
                __typename: "Group",
                name: "group2",
              },
            ],
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
        query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            userEmail: "test@fluidattacks.com",
            userName: "John Doe",
            vulnerabilitiesAssigned: [],
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Navbar).toBe("function");
  });

  it("should render", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions = new PureAbility<string>([]);
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_USER_ORGANIZATIONS_GROUPS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              organizations: {
                __typename: "Organization",
                groups: [
                  {
                    __typename: "Group",
                    name: "testgroup",
                    permissions: ["valid_assigned"],
                    serviceAttributes: [],
                  },
                ],
                name: "okada",
              },
            },
          },
        },
      },
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
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_ID,
          variables: {
            organizationName: "bulat",
          },
        },
        result: {
          data: {
            organizationId: {
              __typename: "Organization",
              id: "ORG#baac1d09-c839-4afd-8ac4-9cbf6434d788",
              name: "bulat",
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_GROUP_NAMES,
          variables: {
            organizationId: "bulat",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              groups: [
                {
                  __typename: "Group",
                  name: "group3",
                },
              ],
              name: "okabulatda",
            },
          },
        },
      },
      {
        request: {
          query: GET_USER_TAGS,
          variables: {
            organizationId: "ORG#baac1d09-c839-4afd-8ac4-9cbf6434d788",
          },
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              tags: [],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_USER_ROLE,
          variables: {
            groupLevel: false,
            groupName: "",
            organizationLevel: true,
            organizationName: "okada",
            userLevel: false,
          },
        },
        result: {
          data: {
            organizationId: {
              __typename: "Organization",
              name: "okada",
              userRole: "user",
            },
          },
        },
      },
    ];

    localStorage.setItem("organization", JSON.stringify({ name: "okada" }));

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
          <MockedProvider
            addTypename={true}
            cache={getCache()}
            mocks={[...mockedOrganizationGroup, ...mockedQueries]}
          >
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                  welcome: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route path={"/orgs/:organizationName"}>
                <Navbar />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("navbar.searchPlaceholder")
      ).toBeInTheDocument();
    });

    expect(screen.getAllByRole("button")[0].textContent).toBe("Okada\u00a0");
    expect(screen.queryByText("bulat")).not.toBeInTheDocument();

    await userEvent.hover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Bulat")).toBeInTheDocument();
    });
    await userEvent.unhover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Bulat")).not.toBeInTheDocument();
    });

    await userEvent.click(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledTimes(0);
    });
    await userEvent.hover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Bulat")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("Bulat"));
    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledTimes(1);
    });

    expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/bulat/groups");

    localStorage.clear();
    jest.clearAllMocks();
  });

  it("should display draft title", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions = new PureAbility<string>([]);
    const organizationsQuery: Readonly<MockedResponse> = {
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
                name: "anotherorg",
              },
            ],
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    };
    const groupServicesQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            serviceAttributes: [],
          },
        },
      },
    };
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF",
        },
      },
      result: {
        data: {
          finding: {
            __typename: "Finding",
            id: "F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF",
            title: "001. Test draft title",
          },
        },
      },
    };

    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={[
            "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF/locations",
          ]}
        >
          <MockedProvider
            addTypename={true}
            cache={getCache()}
            mocks={[
              ...mockedOrganizationGroup,
              groupServicesQuery,
              findingTitleQuery,
              organizationsQuery,
            ]}
          >
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                  welcome: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/drafts/:findingId"
                }
              >
                <Navbar />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByText("001. Test draft title")).toHaveAttribute(
        "href",
        "/orgs/okada/groups/unittesting/drafts/F3F42d73-c1bf-47c5-954e-FFFFFFFFFFFF"
      );
    });

    await userEvent.hover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Anotherorg")).toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });
  });

  it("should display finding title", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockedPermissions = new PureAbility<string>([]);
    const organizationsQuery: Readonly<MockedResponse> = {
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
                name: "secondorg",
              },
            ],
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    };
    const findingTitleQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_FINDING_TITLE,
        variables: {
          findingId: "436992569",
        },
      },
      result: {
        data: {
          finding: {
            id: "436992569",
            title: "001. Test finding title",
          },
        },
      },
    };
    const groupServicesQuery: Readonly<MockedResponse> = {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            serviceAttributes: [],
          },
        },
      },
    };
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <MemoryRouter
          initialEntries={[
            "/orgs/okada/groups/unittesting/vulns/436992569/description",
          ]}
        >
          <MockedProvider
            addTypename={true}
            cache={getCache()}
            mocks={[
              findingTitleQuery,
              groupServicesQuery,
              ...mockedOrganizationGroup,
              organizationsQuery,
            ]}
          >
            <authContext.Provider
              value={{
                tours: {
                  newGroup: true,
                  newRiskExposure: true,
                  newRoot: true,
                  welcome: true,
                },
                userEmail: "test@fluidattacks.com",
                userName: "",
              }}
            >
              <Route
                path={
                  "/orgs/:organizationName/groups/:groupName/vulns/:findingId"
                }
              >
                <Navbar />
              </Route>
            </authContext.Provider>
          </MockedProvider>
        </MemoryRouter>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByText("001. Test finding title")).toHaveAttribute(
        "href",
        "/orgs/okada/groups/unittesting/vulns/436992569"
      );
    });
    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.help.options.expert.title")
      ).toBeInTheDocument();
    });
    await userEvent.hover(screen.getAllByRole("button")[0]);
    await waitFor((): void => {
      expect(screen.queryByText("Secondorg")).toBeInTheDocument();
    });
  });
});
