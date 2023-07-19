import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "./queries";

import { ToDo } from ".";
import {
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "pages/home/dashboard/navbar/breadcrumb/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { getCache } from "utils/apollo";

const mockHistoryPush: jest.Mock = jest.fn();
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

describe("taskInfo component", (): void => {
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

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ToDo).toBe("function");
  });

  it("should list assigned vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockVulnerability: { id: string } = {
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
    };
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned: [mockVulnerability],
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mockedUserAndOrgQueries,
            ...mockedQueries,
            ...mockedQueries,
            ...mockedUserAndOrgQueries,
          ]}
        >
          <ToDo />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor(
      (): void => {
        expect(
          screen.queryByRole("button", { name: "components.navBar.toDo" })
        ).toBeInTheDocument();
      },
      { timeout: 5000 }
    );

    expect(
      screen.queryByText("navbar.task.tooltip.assigned")
    ).not.toBeInTheDocument();

    await userEvent.hover(
      screen.getByRole("button", { name: "components.navBar.toDo" })
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.task.tooltip.assigned")
      ).toBeInTheDocument();
    });

    expect(screen.queryByText("1")).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should not list assigned vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: MockedResponse[] = [
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

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mockedUserAndOrgQueries,
            ...mockedQueries,
            ...mockedQueries,
          ]}
        >
          <ToDo />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("button", { name: "components.navBar.toDo" })
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByText("navbar.task.tooltip.assignedless")
    ).not.toBeInTheDocument();

    await userEvent.hover(
      screen.getByRole("button", { name: "components.navBar.toDo" })
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("navbar.task.tooltip.assignedless")
      ).toBeInTheDocument();
      expect(screen.queryByText("0")).not.toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should handle many assigned vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockVulnerability: { id: string } = {
      id: "89521e9a-b1a3-4047-a16e-15d530dc1340",
    };
    const upperLimit: number = 101;
    const mockedQueries: MockedResponse[] = [
      {
        request: {
          query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        },
        result: {
          data: {
            me: {
              __typename: "Me",
              userEmail: "assigned-user-1",
              vulnerabilitiesAssigned:
                Array(upperLimit).fill(mockVulnerability),
            },
          },
        },
      },
    ];

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mockedUserAndOrgQueries,
            ...mockedQueries,
            ...mockedQueries,
          ]}
        >
          <ToDo />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("button", { name: "components.navBar.toDo" })
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", { name: "components.navBar.toDo" })
    );

    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/todos");
    });

    jest.clearAllMocks();
  });
});
