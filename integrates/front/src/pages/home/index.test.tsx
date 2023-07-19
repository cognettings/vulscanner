import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_USER_REMEMBER } from "./dashboard/legal-notice/queries";
import { GET_USER_ROLE } from "./dashboard/navbar/user-profile/role/queries";
import { GET_CURRENT_USER } from "./queries";
import type { ICurrentUser } from "./queries";

import { Home } from ".";
import { authContext } from "context/auth";
import { GET_STAKEHOLDER_TRIAL } from "hooks/queries";
import { GET_STAKEHOLDER_GROUPS } from "pages/home/auto-enrollment/queries";
import type { IGetStakeholderGroupsResult } from "pages/home/auto-enrollment/types";
import { EMAIL_DOMAINS_URL } from "pages/home/auto-enrollment/utils";
import {
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "pages/home/dashboard/navbar/breadcrumb/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { GET_ORG_EVENTS } from "scenes/Dashboard/components/EventBar/queries";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView/queries";
import {
  GET_ORGANIZATION_ID,
  GET_USER_PORTFOLIOS,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { GET_ORG_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import { getCache } from "utils/apollo";

describe("Home", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Home).toBe("function");
  });

  it("should render NoEnrolledUser component", async (): Promise<void> => {
    expect.hasAssertions();

    const enrollmentMock: MockedResponse<ICurrentUser> = {
      request: {
        query: GET_CURRENT_USER,
      },
      result: {
        data: {
          me: {
            enrolled: false,
            permissions: [],
            phone: null,
            tours: {
              newGroup: true,
              newRiskExposure: true,
              newRoot: true,
              welcome: true,
            },
            trial: {
              completed: true,
            },
            userEmail: "test@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };

    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            trial: null,
            userEmail: "test@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[enrollmentMock, groupsMock]}>
          <authContext.Provider
            value={{
              setUser: jest.fn(),
              tours: {
                newGroup: true,
                newRiskExposure: true,
                newRoot: true,
                welcome: true,
              },
              userEmail: "test@fluidattacks.com",
              userName: "John Doe",
            }}
          >
            <Home />
          </authContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("login.noEnrolledUser.title")
      ).toBeInTheDocument();
    });
  });

  it("should render dashboard", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_USER_REMEMBER,
          variables: {},
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              remember: false,
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: GET_STAKEHOLDER_TRIAL,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              trial: null,
              userEmail: "test@fluidattacks.com",
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
          query: GET_ORG_LEVEL_PERMISSIONS,
          variables: {
            identifier: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
          },
        },
        result: {
          data: {
            organization: {
              __typename: "Organization",
              name: "okada",
              permissions: [],
              userRole: "user",
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
                  name: "testgroup",
                },
              ],
              name: "okada",
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
          query: GET_USER_TAGS,
          variables: {
            organizationId: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
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
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
          },
        },
        result: {
          data: {
            organization: {
              coveredAuthors: 2,
              coveredRepositories: 1,
              groups: [
                {
                  description: "Continuous type test group",
                  events: [],
                  hasAsm: true,
                  hasForces: true,
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "unittesting",
                  openFindings: 1,
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user",
                },
              ],
              missedAuthors: 4,
              missedRepositories: 3,
              name: "okada",
              trial: null,
            },
          },
        },
      },
      {
        request: {
          query: GET_USER_PORTFOLIOS,
          variables: {
            organizationId: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
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
            organizationLevel: false,
            organizationName: "",
            userLevel: true,
          },
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              role: "user",
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

    const enrollmentMock: MockedResponse = {
      request: {
        query: GET_CURRENT_USER,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            enrolled: true,
            permissions: [],
            phone: null,
            tours: {
              newGroup: true,
              newRiskExposure: true,
              newRoot: true,
              welcome: true,
            },
            trial: {
              completed: true,
            },
            userEmail: "test@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };
    const userLevelMock: MockedResponse = {
      request: {
        query: GET_USER_ROLE,
        variables: {
          groupLevel: false,
          groupName: "",
          organizationLevel: false,
          organizationName: "",
          userLevel: true,
        },
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            role: "user",
            userEmail: "test@fluidattacks.com",
          },
        },
      },
    };
    const orgLevelMock: MockedResponse = {
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
    };

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[
            enrollmentMock,
            enrollmentMock,
            userLevelMock,
            orgLevelMock,
            ...mocks,
          ]}
        >
          <authContext.Provider
            value={{
              setUser: jest.fn(),
              tours: {
                newGroup: true,
                newRiskExposure: true,
                newRoot: true,
                welcome: true,
              },
              userEmail: "test@fluidattacks.com",
              userName: "John Doe",
            }}
          >
            <Home />
          </authContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
  });
});
