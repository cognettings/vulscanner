import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { TasksReattacks } from "scenes/Dashboard/containers/Tasks-Content/Reattacks";
import { GET_TODO_REATTACKS } from "scenes/Dashboard/containers/Tasks-Content/Reattacks/queries";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";

jest.mock("utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

const DummyComponent: React.FC = (): JSX.Element => {
  return <div>{"For redirect test only"}</div>;
};

describe("TodoReattacksView", (): void => {
  const mocksReattacks: MockedResponse = {
    request: {
      query: GET_TODO_REATTACKS,
      variables: {
        first: 150,
      },
    },
    result: {
      data: {
        me: {
          findingReattacksConnection: {
            edges: [
              {
                node: {
                  groupName: "group1",
                  id: "436992569",
                  title: "038. Business information leak",
                  verificationSummary: {
                    requested: 23,
                  },
                  vulnerabilitiesToReattackConnection: {
                    edges: [
                      {
                        node: {
                          id: "587c40de-09a0-4d85-a9f9-eaa46aa895d7",
                          lastRequestedReattackDate: "2022-07-12 16:42:53",
                        },
                      },
                    ],
                    pageInfo: {
                      endCursor: "bnVsbA==",
                      hasNextPage: false,
                    },
                    total: 1,
                  },
                },
              },
            ],
            pageInfo: {
              endCursor: "bnVsbA==",
              hasNextPage: false,
            },
            total: 1,
          },
          userEmail: "test@fluidattacks.com",
        },
      },
    },
  };

  const mocksUserGroups: MockedResponse = {
    request: {
      query: GET_USER_ORGANIZATIONS_GROUPS,
    },
    result: {
      data: {
        me: {
          __typename: "Me",
          organizations: [
            {
              groups: [
                {
                  name: "group1",
                  permissions: ["api_mutations_confirm_vulnerabilities_mutate"],
                  serviceAttributes: [],
                },
              ],
              name: "orgtest",
            },
          ],
          userEmail: "test@test.test",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TasksReattacks).toBe("function");
  });

  it("should render table colunms", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/reattacks"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mocksUserGroups, mocksReattacks]}
        >
          <Route component={TasksReattacks} path={"/todos/reattacks"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(screen.queryAllByRole("table")).toHaveLength(1);

    expect(screen.getByText("Type")).toBeInTheDocument();
    expect(screen.getByText("Requested vulns")).toBeInTheDocument();
    expect(screen.getByText("Group name")).toBeInTheDocument();
    expect(screen.getByText("Reattack date")).toBeInTheDocument();

    await waitFor((): void => {
      expect(
        screen.queryByText("038. Business information leak")
      ).toBeInTheDocument();
    });

    expect(screen.getByText("2022-07-12 16:42:53")).toBeInTheDocument();
    expect(screen.getByText("23")).toBeInTheDocument();
    expect(screen.getByText("group1")).toBeInTheDocument();

    jest.clearAllMocks();
  });

  it("should redirect to locations", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/todos/reattacks"]}>
        <MockedProvider
          addTypename={true}
          mocks={[mocksUserGroups, mocksReattacks]}
        >
          <Route component={TasksReattacks} path={"/todos/reattacks"} />
        </MockedProvider>
        <Route
          component={DummyComponent}
          path={"/orgs/orgtest/groups/group1/vulns/436992569/locations"}
        />
      </MemoryRouter>
    );

    expect(screen.queryAllByRole("table")).toHaveLength(1);

    await waitFor((): void => {
      expect(
        screen.queryByText("038. Business information leak")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("038. Business information leak"));

    expect(screen.getByText("For redirect test only")).toBeInTheDocument();

    jest.clearAllMocks();
  });
});
