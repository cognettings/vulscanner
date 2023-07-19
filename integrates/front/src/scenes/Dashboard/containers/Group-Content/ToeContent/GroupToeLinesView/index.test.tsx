import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import {
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GIT_ROOTS } from "./HandleAdditionModal/queries";
import { GET_TOE_LINES, VERIFY_TOE_LINES } from "./queries";

import { GroupToeLinesView } from ".";
import { authzPermissionsContext } from "context/authz/config";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("groupToeLinesView", (): void => {
  const toeLinesQuery = {
    group: {
      __typename: "Group",
      codeLanguages: null,
      name: "unittesting",
      toeLinesConnection: {
        __typename: "ToeLinesConnection",
        edges: [
          {
            __typename: "ToeLinesEdge",
            node: {
              __typename: "ToeLines",
              attackedAt: "2021-02-20T05:00:00+00:00",
              attackedBy: "test2@test.com",
              attackedLines: 4,
              bePresent: true,
              bePresentUntil: "",
              comments: "comment 1",
              filename: "test/test#.config",
              firstAttackAt: "2020-02-19T15:41:04+00:00",
              hasVulnerabilities: false,
              lastAuthor: "user@gmail.com",
              lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
              loc: 8,
              modifiedDate: "2020-11-15T15:41:04+00:00",
              root: {
                __typename: "GitRoot",
                id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                nickname: "universe",
              },
              seenAt: "2020-02-01T15:41:04+00:00",
              sortsPriorityFactor: 70,
              sortsSuggestions: null,
            },
          },
          {
            __typename: "ToeLinesEdge",
            node: {
              __typename: "ToeLines",
              attackedAt: "",
              attackedBy: "test@test.com",
              attackedLines: 120,
              bePresent: false,
              bePresentUntil: "2021-01-01T15:41:04+00:00",
              comments: "comment 2",
              filename: "test2/test.sh",
              firstAttackAt: "",
              hasVulnerabilities: true,
              lastAuthor: "user@gmail.com",
              lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
              loc: 172,
              modifiedDate: "2020-11-16T15:41:04+00:00",
              root: {
                __typename: "GitRoot",
                id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                nickname: "integrates_1",
              },
              seenAt: "2020-01-01T15:41:04+00:00",
              sortsPriorityFactor: 10,
              sortsSuggestions: null,
            },
          },
        ],
        pageInfo: {
          endCursor: "bnVsbA==",
          hasNextPage: false,
        },
        total: 2,
      },
    },
  };
  const queryMock: MockedResponse = {
    request: {
      query: GET_GIT_ROOTS,
      variables: { groupName: "unittesting" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "unittesting",
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
  };
  const mockedToeLines1: MockedResponse = {
    request: {
      query: GET_TOE_LINES,
      variables: {
        attackedBy: undefined,
        bePresent: undefined,
        canGetAttackedAt: true,
        canGetAttackedBy: true,
        canGetAttackedLines: true,
        canGetBePresentUntil: true,
        canGetComments: true,
        canGetFirstAttackAt: true,
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
        sort: {
          field: "SORTS_PRIORITY_FACTOR",
          order: "DESC",
        },
        toAttackedAt: undefined,
        toBePresentUntil: undefined,
        toFirstAttackAt: undefined,
        toModifiedDate: undefined,
        toSeenAt: undefined,
      },
    },
    result: {
      data: toeLinesQuery,
    },
  };
  const mockedToeLines2: MockedResponse = {
    request: {
      query: GET_TOE_LINES,
      variables: {
        attackedBy: undefined,
        bePresent: undefined,
        canGetAttackedAt: true,
        canGetAttackedBy: true,
        canGetAttackedLines: true,
        canGetBePresentUntil: true,
        canGetComments: true,
        canGetFirstAttackAt: true,
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
        sort: {
          field: "SORTS_PRIORITY_FACTOR",
          order: "DESC",
        },
        toAttackedAt: undefined,
        toBePresentUntil: undefined,
        toFirstAttackAt: undefined,
        toModifiedDate: undefined,
        toSeenAt: undefined,
      },
    },
    result: {
      data: toeLinesQuery,
    },
  };

  const mockedPermissions = new PureAbility<string>([
    { action: "api_resolvers_toe_lines_attacked_at_resolve" },
    { action: "api_resolvers_toe_lines_attacked_by_resolve" },
    { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
    { action: "api_mutations_add_toe_lines_mutate" },
    { action: "api_resolvers_toe_lines_be_present_until_resolve" },
    { action: "api_resolvers_toe_lines_comments_resolve" },
    { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
    { action: "see_toe_lines_coverage" },
  ]);

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupToeLinesView).toBe("function");
  });

  it("should display group toe lines", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[mockedToeLines2, queryMock, mockedToeLines1, mockedToeLines2]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getAllByRole("row")[0].textContent?.replace(/[^a-zA-Z ]/gu, "")
    ).toStrictEqual(
      [
        "group.toe.lines.root",
        "group.toe.lines.loc",
        "group.toe.lines.status",
        "group.toe.lines.modifiedDate",
        "group.toe.lines.lastCommit",
        "group.toe.lines.coverage",
        "group.toe.lines.attackedLines",
        "group.toe.lines.attackedAt",
        "group.toe.lines.comments",
      ]
        .join("")
        .replace(/[^a-zA-Z ]/gu, "")
    );
    expect(screen.getAllByRole("row")[2].textContent).toStrictEqual(
      [
        "integrates_1",
        "172",
        "Group.toe.lines.vulnerable",
        "2020-11-16",
        "f9e4beb",
        "70%",
        "120",
        "",
        "comment 2",
      ].join("")
    );
    expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
      [
        "universe",
        "8",
        "Group.toe.lines.safe",
        "2020-11-15",
        "f9e4beb",
        "50%",
        "4",
        "2021-02-20",
        "comment 1",
      ].join("")
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("group.toe.lines.actionButtons.addButton.text")
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByText("group.toe.lines.actionButtons.addButton.text")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.toe.lines.addModal.title")
      ).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should handle verify lines", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test/test#.config",
            groupName: "unittesting",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
            shouldGetNewToeLines: true,
          },
        },
        result: {
          data: {
            updateToeLinesAttackedLines: {
              success: true,
              toeLines: {
                __typename: "ToeLines",
                attackedAt: "2021-02-20T05:00:00+00:00",
                attackedBy: "test2@test.com",
                attackedLines: 8,
                bePresent: true,
                bePresentUntil: "",
                comments: "comment 1",
                filename: "test/test#.config",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                lastAuthor: "user@gmail.com",
                lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc: 8,
                modifiedDate: "2020-11-15T15:41:04+00:00",
                root: {
                  __typename: "GitRoot",
                  id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                  nickname: "universe1",
                },
                seenAt: "2020-02-01T15:41:04+00:00",
                sortsPriorityFactor: 70,
                sortsSuggestions: null,
              },
            },
          },
        },
      },
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test2/test.sh",
            groupName: "unittesting",
            rootId: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
            shouldGetNewToeLines: true,
          },
        },
        result: {
          data: {
            updateToeLinesAttackedLines: {
              success: true,
              toeLines: {
                __typename: "ToeLines",
                attackedAt: "2021-02-20T05:00:00+00:00",
                attackedBy: "test2@test.com",
                attackedLines: 172,
                bePresent: true,
                bePresentUntil: "",
                comments: "comment 1",
                filename: "test2/test.sh",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                lastAuthor: "user@gmail.com",
                lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc: 172,
                modifiedDate: "2020-11-15T15:41:04+00:00",
                root: {
                  __typename: "GitRoot",
                  id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                  nickname: "universe2",
                },
                seenAt: "2020-02-01T15:41:04+00:00",
                sortsPriorityFactor: 70,
                sortsSuggestions: null,
              },
            },
          },
        },
      },
    ];
    const handleMockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_toe_lines_attacked_at_resolve" },
      { action: "api_resolvers_toe_lines_attacked_by_resolve" },
      { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
      { action: "api_resolvers_toe_lines_be_present_until_resolve" },
      { action: "api_resolvers_toe_lines_comments_resolve" },
      { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
      { action: "see_toe_lines_coverage" },
    ]);
    render(
      <MemoryRouter
        initialEntries={[
          "/orgs/okada/groups/unittesting/internal/surface/lines",
        ]}
      >
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            ...mocksMutation,
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={handleMockedPermissions}>
            <Route
              path={
                "/orgs/:organizationName/groups/:groupName/internal/surface/lines"
              }
            >
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
        .textContent
    ).toBe("50%");
    expect(
      within(screen.queryAllByRole("row")[2]).getAllByRole("cell")[5]
        .textContent
    ).toBe("70%");

    expect(
      screen.getByText("group.toe.lines.actionButtons.verifyButton.text")
    ).toBeDisabled();

    await userEvent.click(screen.getAllByRole("checkbox")[1]);
    await userEvent.click(screen.getAllByRole("checkbox")[2]);

    expect(
      screen.getByText("group.toe.lines.actionButtons.verifyButton.text")
    ).not.toBeDisabled();

    await userEvent.click(
      screen.getByText("group.toe.lines.actionButtons.verifyButton.text")
    );

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
          .textContent
      ).toBe("100%");
    });

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.lines.alerts.verifyToeLines.success",
        "groupAlerts.updatedTitle"
      );
    });

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
          .textContent
      ).toBe("100%");
    });

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
          .textContent
      ).toBe("100%");
    });

    expect(
      within(screen.queryAllByRole("row")[2]).getAllByRole("cell")[5]
        .textContent
    ).toBe("100%");
  });

  it("should handle edit attacked lines on cell", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: MockedResponse[] = [
      queryMock,
      mockedToeLines1,
      mockedToeLines2,
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            attackedLines: 6,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test/test#.config",
            groupName: "unittesting",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
            shouldGetNewToeLines: true,
          },
        },
        result: {
          data: {
            updateToeLinesAttackedLines: {
              success: true,
              toeLines: {
                __typename: "ToeLines",
                attackedAt: "2021-02-20T05:00:00+00:00",
                attackedBy: "test2@test.com",
                attackedLines: 6,
                bePresent: true,
                bePresentUntil: "",
                comments: "comment 1",
                filename: "test/test#.config",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                lastAuthor: "user@gmail.com",
                lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc: 8,
                modifiedDate: "2020-11-15T15:41:04+00:00",
                root: {
                  __typename: "GitRoot",
                  id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                  nickname: "universe",
                },
                seenAt: "2020-02-01T15:41:04+00:00",
                sortsPriorityFactor: 70,
                sortsSuggestions: null,
              },
            },
          },
        },
      },
    ];
    const handleMockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_toe_lines_attacked_at_resolve" },
      { action: "api_resolvers_toe_lines_attacked_by_resolve" },
      { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
      { action: "api_resolvers_toe_lines_be_present_until_resolve" },
      { action: "api_resolvers_toe_lines_comments_resolve" },
      { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
      { action: "see_toe_lines_coverage" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            mockedToeLines2,
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={handleMockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
        .textContent
    ).toBe("50%");

    await userEvent.dblClick(
      screen.getAllByRole("button", { name: "plus" })[0]
    );
    await userEvent.type(screen.getAllByRole("spinbutton")[0], "{enter}");

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.lines.alerts.verifyToeLines.success",
        "groupAlerts.updatedTitle"
      );
    });

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
          .textContent
      ).toBe("75%");
    });

    expect(screen.getAllByRole("spinbutton")[0]).toHaveValue(6);
  });

  it("should handle edit attacked lines on cell errors", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mocksMutation: MockedResponse[] = [
      queryMock,
      mockedToeLines1,
      mockedToeLines2,
      {
        request: {
          query: VERIFY_TOE_LINES,
          variables: {
            attackedLines: 8,
            canGetAttackedAt: true,
            canGetAttackedBy: true,
            canGetAttackedLines: true,
            canGetBePresentUntil: true,
            canGetComments: true,
            canGetFirstAttackAt: true,
            filename: "test/test#.config",
            groupName: "unittesting",
            rootId: "63298a73-9dff-46cf-b42d-9b2f01a56690",
            shouldGetNewToeLines: true,
          },
        },
        result: {
          errors: [
            new GraphQLError(
              "Exception - The toe lines has been updated by another operation"
            ),
            new GraphQLError(
              "Exception - The attacked lines must be between 0 and the loc (lines of code)"
            ),
            new GraphQLError("Unexpected error"),
          ],
        },
      },
    ];
    const handleMockedPermissions = new PureAbility<string>([
      { action: "api_resolvers_toe_lines_attacked_at_resolve" },
      { action: "api_resolvers_toe_lines_attacked_by_resolve" },
      { action: "api_resolvers_toe_lines_attacked_lines_resolve" },
      { action: "api_resolvers_toe_lines_be_present_until_resolve" },
      { action: "api_resolvers_toe_lines_comments_resolve" },
      { action: "api_resolvers_toe_lines_first_attack_at_resolve" },
      { action: "api_mutations_update_toe_lines_attacked_lines_mutate" },
      { action: "see_toe_lines_coverage" },
    ]);
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            ...mocksMutation,
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={handleMockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      within(screen.queryAllByRole("row")[1]).getAllByRole("cell")[5]
        .textContent
    ).toBe("50%");

    await userEvent.tripleClick(
      screen.getAllByRole("button", { name: "plus" })[0]
    );
    await userEvent.click(screen.getAllByRole("button", { name: "plus" })[0]);

    await userEvent.type(screen.getAllByRole("spinbutton")[0], "{enter}");

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(3);
    });
  });

  it("should have filters", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockedQueries: MockedResponse[] = [
      queryMock,
      mockedToeLines1,
      mockedToeLines2,
    ];

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[...mockedQueries, ...mockedQueries]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    expect(
      screen.getByRole("textbox", { name: "filename" })
    ).toBeInTheDocument();
    expect(screen.getAllByRole("spinbutton", { name: "loc" })).toHaveLength(2);
    expect(
      screen.getByRole("combobox", { name: "hasVulnerabilities" })
    ).toBeInTheDocument();
    expect(
      document.querySelectorAll(`input[name="modifiedDate"]`)
    ).toHaveLength(2);
    expect(
      screen.getByRole("textbox", { name: "lastCommit" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "lastAuthor" })
    ).toBeInTheDocument();
    expect(document.querySelectorAll(`input[name="seenAt"]`)).toHaveLength(2);
    expect(
      screen.getAllByRole("spinbutton", { name: "sortsPriorityFactor" })
    ).toHaveLength(2);
    expect(
      screen.getByRole("combobox", { name: "bePresent" })
    ).toBeInTheDocument();
    expect(
      screen.getAllByRole("spinbutton", { name: "attackedLines" })
    ).toHaveLength(2);
    expect(document.querySelectorAll(`input[name="attackedAt"]`)).toHaveLength(
      2
    );
    expect(
      screen.getByRole("textbox", { name: "attackedBy" })
    ).toBeInTheDocument();
    expect(
      document.querySelectorAll(`input[name="firstAttackAt"]`)
    ).toHaveLength(2);
    expect(
      screen.getByRole("textbox", { name: "comments" })
    ).toBeInTheDocument();
    expect(
      document.querySelectorAll(`input[name="bePresentUntil"]`)
    ).toHaveLength(2);
  });

  it("should filter by filename", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: "test/test#.config",
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "filename" }), {
      target: { value: "test/test#.config" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by loc", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          minLoc: 170,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getAllByRole("spinbutton", { name: "loc" })[0], {
      target: { value: 170 },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by modified date", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: undefined,
          fromBePresentUntil: undefined,
          fromFirstAttackAt: undefined,
          fromModifiedDate: "2020-11-16T00:00:00.000Z",
          fromSeenAt: undefined,
          groupName: "unittesting",
          hasVulnerabilities: undefined,
          lastAuthor: undefined,
          lastCommit: undefined,
          maxAttackedLines: undefined,
          maxLoc: undefined,
          maxSortsPriorityFactor: undefined,
          minAttackedLines: undefined,
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: "",
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      document.querySelectorAll(`input[name="modifiedDate"]`)[0],
      {
        target: { value: "2020-11-16" },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by last commit", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
          maxAttackedLines: undefined,
          maxLoc: undefined,
          maxSortsPriorityFactor: undefined,
          minAttackedLines: undefined,
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "lastCommit" }), {
      target: { value: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by last author", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          lastAuthor: "user@gmail.com",
          lastCommit: undefined,
          maxAttackedLines: undefined,
          maxLoc: undefined,
          maxSortsPriorityFactor: undefined,
          minAttackedLines: undefined,
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "lastAuthor" }), {
      target: { value: "user@gmail.com" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });
  });

  it("should filter by seen at", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: undefined,
          fromBePresentUntil: undefined,
          fromFirstAttackAt: undefined,
          fromModifiedDate: undefined,
          fromSeenAt: "2020-02-01T00:00:00.000Z",
          groupName: "unittesting",
          hasVulnerabilities: undefined,
          lastAuthor: undefined,
          lastCommit: undefined,
          maxAttackedLines: undefined,
          maxLoc: undefined,
          maxSortsPriorityFactor: undefined,
          minAttackedLines: undefined,
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: "",
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(document.querySelectorAll(`input[name="seenAt"]`)[0], {
      target: { value: "2020-02-01" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by sorts risk level", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          minLoc: undefined,
          minSortsPriorityFactor: 79,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "sortsPriorityFactor" })[0],
      {
        target: { value: 79 },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by be present", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: true,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("combobox", { name: "bePresent" }), {
      target: { value: true },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by has vulnerabilities", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: undefined,
          fromBePresentUntil: undefined,
          fromFirstAttackAt: undefined,
          fromModifiedDate: undefined,
          fromSeenAt: undefined,
          groupName: "unittesting",
          hasVulnerabilities: true,
          lastAuthor: undefined,
          lastCommit: undefined,
          maxAttackedLines: undefined,
          maxLoc: undefined,
          maxSortsPriorityFactor: undefined,
          minAttackedLines: undefined,
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      screen.getByRole("combobox", { name: "hasVulnerabilities" }),
      {
        target: { value: true },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by attacked lines", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          minAttackedLines: 119,
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "attackedLines" })[0],
      {
        target: { value: 119 },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by attacked at", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: "2021-02-19T00:00:00.000Z",
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: "",
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(document.querySelectorAll(`input[name="attackedAt"]`)[0], {
      target: { value: "2021-02-19" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by attacked by", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: "test@test.com",
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "attackedBy" }), {
      target: { value: "test@test.com" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by first attack at", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: undefined,
          fromBePresentUntil: undefined,
          fromFirstAttackAt: "2020-02-18T00:00:00.000Z",
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: "",
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      document.querySelectorAll(`input[name="firstAttackAt"]`)[0],
      {
        target: { value: "2020-02-18" },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by comments", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: "comment 1",
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          rootId: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: undefined,
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(screen.getByRole("textbox", { name: "comments" }), {
      target: { value: "comment 1" },
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by be present until", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedFilteredToeLines: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          fromAttackedAt: undefined,
          fromBePresentUntil: "2021-01-01T00:00:00.000Z",
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
          minLoc: undefined,
          minSortsPriorityFactor: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
          toAttackedAt: undefined,
          toBePresentUntil: "",
          toFirstAttackAt: undefined,
          toModifiedDate: undefined,
          toSeenAt: undefined,
        },
      },
      result: {
        data: toeLinesQuery,
      },
    };

    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedFilteredToeLines,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      document.querySelectorAll(`input[name="bePresentUntil"]`)[0],
      {
        target: { value: "2021-01-01" },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should filter by min coverage", async (): Promise<void> => {
    expect.hasAssertions();

    const toeLinesMockCoverage = {
      group: {
        __typename: "Group",
        codeLanguages: null,
        name: "unittesting",
        toeLinesConnection: {
          __typename: "ToeLinesConnection",
          edges: [
            {
              __typename: "ToeLinesEdge",
              node: {
                __typename: "ToeLines",
                attackedAt: "",
                attackedBy: "test@test.com",
                attackedLines: 120,
                bePresent: false,
                bePresentUntil: "2021-01-01T15:41:04+00:00",
                comments: "comment 2",
                filename: "test2/test.sh",
                firstAttackAt: "",
                hasVulnerabilities: true,
                lastAuthor: "user@gmail.com",
                lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c1",
                loc: 172,
                modifiedDate: "2020-11-16T15:41:04+00:00",
                root: {
                  __typename: "GitRoot",
                  id: "765b1d0f-b6fb-4485-b4e2-2c2cb1555b1a",
                  nickname: "integrates_1",
                },
                seenAt: "2020-01-01T15:41:04+00:00",
                sortsPriorityFactor: 10,
                sortsSuggestions: null,
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
    };

    const mockedToeLinesCoverage: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          groupName: "unittesting",
          maxCoverage: undefined,
          minCoverage: 52,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
        },
      },
      result: {
        data: toeLinesMockCoverage,
      },
    };
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedToeLinesCoverage,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "coverage" })[0],
      {
        target: { value: 52 },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    expect(screen.getByText("integrates_1")).toBeInTheDocument();
  });

  it("should filter by max coverage", async (): Promise<void> => {
    expect.hasAssertions();

    const toeLinesMockCoverage = {
      group: {
        __typename: "Group",
        codeLanguages: null,
        name: "unittesting",
        toeLinesConnection: {
          __typename: "ToeLinesConnection",
          edges: [
            {
              __typename: "ToeLinesEdge",
              node: {
                __typename: "ToeLines",
                attackedAt: "2021-02-20T05:00:00+00:00",
                attackedBy: "test2@test.com",
                attackedLines: 4,
                bePresent: true,
                bePresentUntil: "",
                comments: "comment 1",
                filename: "test/test#.config",
                firstAttackAt: "2020-02-19T15:41:04+00:00",
                hasVulnerabilities: false,
                lastAuthor: "user@gmail.com",
                lastCommit: "f9e4beba70c4f34d6117c3b0c23ebe6b2bff66c2",
                loc: 8,
                modifiedDate: "2020-11-15T15:41:04+00:00",
                root: {
                  __typename: "GitRoot",
                  id: "63298a73-9dff-46cf-b42d-9b2f01a56690",
                  nickname: "universe",
                },
                seenAt: "2020-02-01T15:41:04+00:00",
                sortsPriorityFactor: 70,
                sortsSuggestions: null,
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
    };

    const mockedToeLinesCoverage: MockedResponse = {
      request: {
        query: GET_TOE_LINES,
        variables: {
          attackedBy: undefined,
          bePresent: undefined,
          canGetAttackedAt: true,
          canGetAttackedBy: true,
          canGetAttackedLines: true,
          canGetBePresentUntil: true,
          canGetComments: true,
          canGetFirstAttackAt: true,
          comments: undefined,
          filename: undefined,
          first: 150,
          groupName: "unittesting",
          maxCoverage: 50,
          minCoverage: undefined,
          sort: {
            field: "SORTS_PRIORITY_FACTOR",
            order: "DESC",
          },
        },
      },
      result: {
        data: toeLinesMockCoverage,
      },
    };
    render(
      <MemoryRouter initialEntries={["/unittesting/surface/lines"]}>
        <MockedProvider
          addTypename={true}
          cache={getCache()}
          mocks={[
            queryMock,
            mockedToeLines1,
            mockedToeLines2,
            mockedToeLinesCoverage,
            queryMock,
            mockedToeLines2,
          ]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route path={"/:groupName/surface/lines"}>
              <GroupToeLinesView isInternal={true} />
            </Route>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    const numberOfRows: number = 3;

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(numberOfRows);
    });

    expect(
      screen.getByRole("button", { name: "Add filter" })
    ).toBeInTheDocument();

    await userEvent.click(screen.getByRole("button", { name: "Add filter" }));

    fireEvent.change(
      screen.getAllByRole("spinbutton", { name: "coverage" })[1],
      {
        target: { value: 50 },
      }
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });

    expect(screen.getByText("universe")).toBeInTheDocument();
  });
});
