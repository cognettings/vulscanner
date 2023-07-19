import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GIT_ROOTS } from "./GroupToeLinesView/HandleAdditionModal/queries";

import { authzPermissionsContext } from "context/authz/config";
import { ToeContent } from "scenes/Dashboard/containers/Group-Content/ToeContent/";
import { GET_TOE_LINES } from "scenes/Dashboard/containers/Group-Content/ToeContent/GroupToeLinesView/queries";
import { getCache } from "utils/apollo";

describe("ToeContent", (): void => {
  const mockedToeLines: MockedResponse[] = [
    {
      request: {
        query: GET_TOE_LINES,
        variables: {
          bePresent: undefined,
          canGetAttackedAt: false,
          canGetAttackedBy: false,
          canGetAttackedLines: false,
          canGetBePresentUntil: false,
          canGetComments: false,
          canGetFirstAttackAt: false,
          first: 150,
          groupName: "unittesting",
          minLoc: 1,
          rootId: undefined,
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            codeLanguages: null,
            name: "unittesting",
            toeLinesConnection: {
              __typename: "ToeLinesConnection",
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
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: false,
          canGetAttackedBy: false,
          canGetAttackedLines: false,
          canGetBePresentUntil: false,
          canGetComments: false,
          canGetFirstAttackAt: false,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: undefined,
          fromBePresentUntil: undefined,
          fromFirstAttackAt: undefined,
          fromModifiedDate: undefined,
          fromSeenAt: undefined,
          groupName: "unittesting",
          hasVulnerabilities: undefined,
          lastAuthor: undefined,
          lastCommit: undefined,
          maxAttackedLines: undefined,
          maxLoc: undefined,
          maxSortsPriorityFactor: undefined,
          minAttackedLines: undefined,
          minLoc: 1,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: { field: "SORTS_PRIORITY_FACTOR", order: "DESC" },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            codeLanguages: null,
            name: "unittesting",
            toeLinesConnection: {
              __typename: "ToeLinesConnection",
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
        query: GET_GIT_ROOTS,
        variables: { groupName: "unittesting" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "test",
            roots: [
              {
                __typename: "GitRoot",
                id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
                nickname: "universe",
                state: "ACTIVE",
              },
            ],
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ToeContent).toBe("function");
  });

  it("should display toe tabs", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_group_toe_lines_connection_resolve" },
      { action: "api_resolvers_group_toe_inputs_resolve" },
      { action: "api_resolvers_group_toe_ports_resolve" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedToeLines, ...mockedToeLines]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface"}>
              <ToeContent isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(4);
    });

    expect(
      screen.getByRole("link", { name: "group.toe.tabs.lines.text" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.inputs.text" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.ports.text" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.lines.text" })
    ).toHaveClass("active");
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.inputs.text" })
    ).not.toHaveClass("active");
    expect(
      screen.getByRole("link", { name: "group.toe.tabs.ports.text" })
    ).not.toHaveClass("active");

    jest.clearAllMocks();
  });
});
