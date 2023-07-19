import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_VERIFIED_FINDING_INFO } from "./AffectedReattackAccordion/queries";
import { GET_FINDING_VULNS_TO_REATTACK } from "./AffectedReattackAccordion/VulnerabilitiesToReattackTable/queries";

import { UPDATE_EVIDENCE_MUTATION } from "../GroupRoute/EventContent/EventEvidenceView/queries";
import { GET_ROOTS } from "../GroupScopeView/queries";
import { authzPermissionsContext } from "context/authz/config";
import { GroupEventsView } from "scenes/Dashboard/containers/Group-Content/GroupEventsView";
import {
  ADD_EVENT_MUTATION,
  GET_EVENTS,
  REQUEST_EVENT_VERIFICATION_MUTATION,
} from "scenes/Dashboard/containers/Group-Content/GroupEventsView/queries";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";

const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("eventsView", (): void => {
  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_EVENTS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
    {
      request: {
        query: GET_VERIFIED_FINDING_INFO,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];
  const mockedVerified: MockedResponse = {
    request: {
      query: GET_VERIFIED_FINDING_INFO,
      variables: {
        groupName: "unittesting",
      },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          findings: [],
          name: "unittesting",
        },
      },
    },
  };
  const mockedRoots: MockedResponse = {
    request: {
      query: GET_ROOTS,
      variables: { groupName: "unittesting" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "unittesting",
          roots: [],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupEventsView).toBe("function");
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
    jest.clearAllMocks();
  });

  it("should render events table and go to event", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      mockedVerified,
    ];

    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider cache={getCache()} mocks={mocks}>
          <Route
            component={GroupEventsView}
            path={"/groups/:groupName/events"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByRole("table")).toBeInTheDocument();
      expect(
        screen.getByRole("cell", { name: "Authorization for a special attack" })
      ).toBeInTheDocument();
      expect(screen.getByRole("cell", { name: "Solved" })).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("cell", { name: "Authorization for a special attack" })
    );

    expect(mockHistoryPush).toHaveBeenCalledWith(
      "/groups/unittesting/events/463457733/description"
    );

    jest.clearAllMocks();
  });

  it("should render new event modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      mockedVerified,
      mockedRoots,
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_event_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider cache={getCache()} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.btn.text")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.events.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText("group.events.new")).toBeInTheDocument();
    });

    expect(screen.getAllByText("group.events.form.date")).toHaveLength(1);
    expect(screen.getAllByRole("combobox", { name: "eventType" })).toHaveLength(
      1
    );
    expect(
      screen.getAllByRole("combobox", { name: "rootNickname" })
    ).toHaveLength(1);
    expect(screen.getAllByRole("textbox", { name: "detail" })).toHaveLength(1);
    expect(screen.getAllByTestId("files")).toHaveLength(1);
    expect(screen.getAllByTestId("images")).toHaveLength(1);

    jest.clearAllMocks();
  });

  it("should render add event", async (): Promise<void> => {
    expect.hasAssertions();

    const images = [
      new File(
        ["okada-unittesting-0192837465"],
        "okada-unittesting-0192837465.png",
        { type: "image/png" }
      ),
      new File(
        ["okada-unittesting-5647382910"],
        "okada-unittesting-0192837465.png",
        { type: "image/png" }
      ),
    ];
    const file = new File(
      ["okada-unittesting-56789abcde"],
      "okada-unittesting-56789abcde.txt",
      {
        type: "text/plain",
      }
    );

    const mockedQueries: readonly MockedResponse[] = [
      mockedVerified,
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: {
                    __typename: "GitRoot",
                    id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    nickname: "universe",
                  },
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: GET_ROOTS,
          variables: { groupName: "unittesting" },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              codeLanguages: null,
              name: "unittesting",
              roots: [
                {
                  __typename: "GitRoot",
                  branch: "master",
                  cloningStatus: {
                    __typename: "GitRootCloningStatus",
                    message: "root created",
                    status: "UNKNOWN",
                  },
                  createdAt: "2022-02-10T14:58:10+00:00",
                  createdBy: "testuser1@test.test",
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    isToken: false,
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  gitEnvironmentUrls: [],
                  gitignore: ["bower_components/*", "node_modules/*"],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: true,
                  lastEditedAt: "2022-10-21T15:58:31+00:00",
                  lastEditedBy: "testuser2@test.test",
                  nickname: "universe",
                  state: "ACTIVE",
                  url: "https://gitlab.com/fluidattacks/universe",
                  useVpn: false,
                },
              ],
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: ADD_EVENT_MUTATION,
          variables: {
            detail: "detail test",
            eventDate: "2021-09-07T00:00:00Z",
            eventType: "CLONING_ISSUES",
            groupName: "unittesting",
            rootId: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          },
        },
        result: {
          data: {
            addEvent: {
              eventId: "123",
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_EVIDENCE_MUTATION,
          variables: {
            eventId: "123",
            evidenceType: "IMAGE_1",
            file: images[0],
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            updateEventEvidence: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_EVIDENCE_MUTATION,
          variables: {
            eventId: "123",
            evidenceType: "IMAGE_2",
            file: images[1],
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            updateEventEvidence: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_EVIDENCE_MUTATION,
          variables: {
            eventId: "123",
            evidenceType: "FILE_1",
            file,
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            updateEventEvidence: {
              success: true,
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_event_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["orgs/okada/groups/unittesting/events"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedQueries, ...mockedMutations, ...mockedQueries]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"orgs/:organizationName/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.btn.text")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.events.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText("group.events.new")).toBeInTheDocument();
    });

    expect(screen.getByRole("button", { name: /confirm/iu })).toBeDisabled();

    await userEvent.type(
      screen.getByRole("combobox", { name: "rootNickname" }),
      "universe"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "detail" }),
      "detail test"
    );

    // 09/07/2021 12:00 AM
    await userEvent.type(
      screen.getByPlaceholderText("mm/dd/yyyy hh:mm (a|p)m"),
      "090720211200A"
    );

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "eventType" }),
      ["group.events.type.cloningIssues"]
    );
    await userEvent.upload(screen.getByTestId("images"), images);
    await userEvent.upload(screen.getByTestId("files"), file);
    await waitFor((): void => {
      expect(
        screen.getByRole("button", { name: /confirm/iu })
      ).not.toBeDisabled();
    });
    await userEvent.click(screen.getByRole("button", { name: /confirm/iu }));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.successCreate",
        "group.events.titleSuccess"
      );
    });
    jest.clearAllMocks();
  });

  it("should handle error adding event in file", async (): Promise<void> => {
    expect.hasAssertions();

    const images = [
      new File(
        ["okada-unittesting-0192837465"],
        "okada-unittesting-0192837465.txt",
        { type: "text/plain" }
      ),
    ];
    const file = new File(
      ["okada-unittesting-56789abcde"],
      "okada-unittesting-56789abcde.img",
      {
        type: "image/png",
      }
    );

    const mockedQueries: readonly MockedResponse[] = [
      mockedVerified,
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: {
                    __typename: "GitRoot",
                    id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    nickname: "universe",
                  },
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: GET_ROOTS,
          variables: { groupName: "unittesting" },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              codeLanguages: null,
              name: "unittesting",
              roots: [
                {
                  __typename: "GitRoot",
                  branch: "master",
                  cloningStatus: {
                    __typename: "GitRootCloningStatus",
                    message: "root created",
                    status: "UNKNOWN",
                  },
                  createdAt: "2022-02-10T14:58:10+00:00",
                  createdBy: "testuser1@test.test",
                  credentials: {
                    __typename: "Credentials",
                    id: "",
                    isToken: false,
                    name: "",
                    type: "",
                  },
                  environment: "production",
                  environmentUrls: [],
                  gitEnvironmentUrls: [],
                  gitignore: ["bower_components/*", "node_modules/*"],
                  id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: true,
                  lastEditedAt: "2022-10-21T15:58:31+00:00",
                  lastEditedBy: "testuser2@test.test",
                  nickname: "universe",
                  state: "ACTIVE",
                  url: "https://gitlab.com/fluidattacks/universe",
                  useVpn: false,
                },
              ],
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: ADD_EVENT_MUTATION,
          variables: {
            detail: "detail test",
            eventDate: "2021-09-07T00:00:00Z",
            eventType: "CLONING_ISSUES",
            groupName: "unittesting",
            rootId: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - Invalid file type: EVENT_IMAGE"),
            new GraphQLError("Exception - Invalid file type: EVENT_FILE"),
            new GraphQLError("Exception - Invalid characters"),
          ],
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_event_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["orgs/okada/groups/unittesting/events"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"orgs/:organizationName/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryByText("group.events.btn.text")).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText("group.events.btn.text"));
    await waitFor((): void => {
      expect(screen.queryByText("group.events.new")).toBeInTheDocument();
    });

    expect(screen.getByRole("button", { name: /confirm/iu })).toBeDisabled();

    await userEvent.type(
      screen.getByRole("combobox", { name: "rootNickname" }),
      "universe"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "detail" }),
      "detail test"
    );

    // 09/07/2021 12:00 AM
    await userEvent.type(
      screen.getByPlaceholderText("mm/dd/yyyy hh:mm (a|p)m"),
      "090720211200A"
    );

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "eventType" }),
      ["group.events.type.cloningIssues"]
    );
    await userEvent.upload(screen.getByTestId("images"), images);
    await userEvent.upload(screen.getByTestId("files"), file);
    await waitFor((): void => {
      expect(
        screen.getByRole("button", { name: /confirm/iu })
      ).not.toBeDisabled();
    });
    await userEvent.click(screen.getByRole("button", { name: /confirm/iu }));

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(3);
    });
    jest.clearAllMocks();
  });

  it("should request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      mockedVerified,
      mockedRoots,
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "CREATED",
                  eventType: "NETWORK_ACCESS_ISSUES",
                  groupName: "unittesting",
                  id: "12314123",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      {
        request: {
          query: REQUEST_EVENT_VERIFICATION_MUTATION,
          variables: {
            comments: "The solution test",
            eventId: "12314123",
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            requestEventVerification: {
              success: true,
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_request_event_verification_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedQueries, ...mockedMutations, ...mockedQueries]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("cell", { name: "Network access issues" })
      ).toBeInTheDocument();
    });

    const row = screen.getByRole("row", {
      name: /12314123 2018-10-17 00:00:00 test description network access issues unsolved -/iu,
    });
    await userEvent.click(within(row).getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: true })[0]
      ).toBeInTheDocument();
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: /group.events.remediationmodal.btn.text/iu,
      })
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: /treatmentjustification/iu }),
      "The solution test"
    );
    await userEvent.click(
      screen.getByRole("button", { name: /components\.modal\.confirm/iu })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.events.successRequestVerification",
        "groupAlerts.updatedTitle"
      );
    });
    jest.clearAllMocks();
  });

  it("should handle error in request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
                {
                  closingDate: "-",
                  detail: "Test description",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "CREATED",
                  eventType: "NETWORK_ACCESS_ISSUES",
                  groupName: "unittesting",
                  id: "12314123",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
    ];
    const mockedMutations: MockedResponse[] = [
      mockedVerified,
      {
        request: {
          query: REQUEST_EVENT_VERIFICATION_MUTATION,
          variables: {
            comments: "The solution test",
            eventId: "463457733",
            groupName: "unittesting",
          },
        },
        result: {
          errors: [
            new GraphQLError("Exception - The event has already been closed"),
          ],
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_request_event_verification_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedQueries, ...mockedMutations]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("cell", { name: "Network access issues" })
      ).toBeInTheDocument();
    });

    const rowUnSlv = screen.getByRole("row", {
      name: /12314123 2018-10-17 00:00:00 test description network access issues unsolved -/iu,
    });
    await userEvent.click(within(rowUnSlv).getByRole("checkbox"));

    const rowSolv = screen.getByRole("row", {
      name: /463457733 2018-10-17 00:00:00 Test description Authorization for a special attack solved -/iu,
    });
    await userEvent.click(within(rowSolv).getByRole("checkbox"));
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        3
      );
    });

    await userEvent.click(
      screen.getByRole("button", {
        name: /group.events.remediationmodal.btn.text/iu,
      })
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("group.events.selectedError");
    });

    expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
      2
    );

    jest.clearAllMocks();
  });

  it("should render update affected reattacks modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedQueries: readonly MockedResponse[] = [
      {
        request: {
          query: GET_EVENTS,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              events: [
                {
                  closingDate: "-",
                  detail: "Test description solved",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "SOLVED",
                  eventType: "AUTHORIZATION_SPECIAL_ATTACK",
                  groupName: "unittesting",
                  id: "463457733",
                  root: null,
                },
                {
                  closingDate: "-",
                  detail: "Test description unsolved",
                  eventDate: "2018-10-17 00:00:00",
                  eventStatus: "CREATED",
                  eventType: "NETWORK_ACCESS_ISSUES",
                  groupName: "unittesting",
                  id: "12314123",
                  root: null,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: GET_VERIFIED_FINDING_INFO,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              findings: [
                {
                  id: "test-finding-id-01",
                  title: "038. Business information leak",
                  verified: false,
                },
                {
                  id: "test-finding-id-02",
                  title: "083. XML injection (XXE)",
                  verified: true,
                },
              ],
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: GET_FINDING_VULNS_TO_REATTACK,
          variables: {
            findingId: "test-finding-id-01",
          },
        },
        result: {
          data: {
            finding: {
              id: "test-finding-id-01",
              vulnerabilitiesToReattackConnection: {
                edges: [
                  {
                    node: {
                      findingId: "test-finding-id-01",
                      id: "test-vuln-id",
                      specific: "1111",
                      where: "vulnerable entrance",
                    },
                  },
                ],
                pageInfo: {
                  endCursor: "cursor",
                  hasNextPage: false,
                },
              },
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_request_vulnerabilities_hold_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider cache={getCache()} mocks={mockedQueries}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("cell", { name: "Network access issues" })
      ).toBeInTheDocument();
    });

    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: "group.events.form.affectedReattacks.btn.text",
        })
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByRole("button", {
        name: "group.events.form.affectedReattacks.btn.text",
      })
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.events.form.affectedReattacks.title")
      ).toBeInTheDocument();
      expect(
        screen.getByRole("combobox", { name: "eventId" })
      ).toBeInTheDocument();
      expect(
        screen.getByText("038. Business information leak")
      ).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should render a error in update affected reattacks modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_request_vulnerabilities_hold_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/groups/unittesting/events"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupEventsView}
              path={"/groups/:groupName/events"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });
});
