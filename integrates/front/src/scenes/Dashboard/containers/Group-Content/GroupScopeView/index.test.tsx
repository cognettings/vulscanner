import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import {
  GET_FILES,
  GET_GROUP_ACCESS_INFO,
  GET_GROUP_DATA,
  GET_TAGS,
} from "./GroupSettingsView/queries";

import { GET_ORGANIZATION_CREDENTIALS as GET_CREDENTIALS_FROM_OAUTH_FORM } from "../../../components/AddOauthRootForm/queries";
import { GET_GROUP_POLICIES } from "../../Organization-Content/PoliciesView/Group/queries";
import { authContext } from "context/auth";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { UPDATE_TOURS } from "hooks/queries";
import { GroupScopeView } from "scenes/Dashboard/containers/Group-Content/GroupScopeView";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  DEACTIVATE_ROOT,
  GET_GROUPS,
  GET_ORGANIZATION_CREDENTIALS,
  GET_ROOTS,
  GET_ROOTS_VULNS,
  UPDATE_GIT_ROOT,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/queries";
import { groupContext } from "scenes/Dashboard/group/context";
import { getCache } from "utils/apollo";

describe("GroupScopeView", (): void => {
  const btnConfirm = "components.modal.confirm";
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FILES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          resources: {
            files: [],
            groupName: "unittesting",
          },
        },
      },
    },
    {
      request: {
        query: GET_TAGS,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "unittesting",
            tags: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "unittesting",
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
            name: "unittesting",
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
        query: GET_GROUP_POLICIES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            maxAcceptanceDays: null,
            maxAcceptanceSeverity: 10,
            maxNumberAcceptances: null,
            minAcceptanceSeverity: 0,
            minBreakingSeverity: null,
            name: "unittesting",
            vulnerabilityGracePeriod: null,
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_ACCESS_INFO,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            disambiguation: "",
            groupContext: "",
            name: "unittesting",
          },
        },
      },
    },
    {
      request: {
        query: GET_ORGANIZATION_CREDENTIALS,
        variables: {
          organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            credentials: [],
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: GET_CREDENTIALS_FROM_OAUTH_FORM,
        variables: {
          organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            credentials: [],
            name: "okada",
          },
        },
      },
    },
    {
      request: {
        query: UPDATE_TOURS,
        variables: {
          newGroup: true,
          newRiskExposure: true,
          newRoot: true,
          welcome: true,
        },
      },
      result: {
        data: {
          updateTours: { success: true },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupScopeView).toBe("function");
  });

  it("should render git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const queryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_service_white" }])}
        >
          <groupContext.Provider
            value={{
              organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
              path: "",
              url: "",
            }}
          >
            <MemoryRouter
              initialEntries={["/orgs/okada/groups/unittesting/scope"]}
            >
              <MockedProvider cache={getCache()} mocks={[...mocks, queryMock]}>
                <Route
                  component={GroupScopeView}
                  path={"/orgs/:organizationName/groups/:groupName/scope"}
                />
              </MockedProvider>
            </MemoryRouter>
          </groupContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("table")[0]).queryByText(
          "table.noDataIndication"
        )
      ).not.toBeInTheDocument();
    });

    expect(
      within(screen.queryAllByRole("table")[0]).queryAllByRole("row")
    ).toHaveLength(2);

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("table")[0]).queryAllByRole("row")[1]
          .textContent
      ).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HealthCheck
          "group.scope.git.healthCheck.yes",
        ].join("")
      );
    });
  });

  it("should add git roots with user credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
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
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          credentials: {
            azureOrganization: undefined,
            isPat: false,
            key: undefined,
            name: "credential name",
            password: "password-test",
            token: "",
            type: "HTTPS",
            user: "user-test",
          },
          environment: "production",
          gitignore: [],
          groupName: "unittesting",
          includesHealthCheck: false,
          nickname: "",
          url: "https://gitlab.com/fluidattacks/universe",
          useVpn: false,
        },
      },
      result: {
        data: { addGitRoot: { __typename: "SimplePayload", success: true } },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
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
    };
    jest.clearAllMocks();

    render(
      <authContext.Provider
        value={{
          setUser: jest.fn(),
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={
            new PureAbility([
              { action: "has_service_white" },
              { action: "has_squad" },
            ])
          }
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_add_secret_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <groupContext.Provider
              value={{
                organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
                path: "",
                url: "",
              }}
            >
              <MemoryRouter
                initialEntries={["/orgs/okada/groups/unittesting/scope"]}
              >
                <MockedProvider
                  cache={getCache()}
                  mocks={[
                    ...mocks,
                    initialQueryMock,
                    mutationMock,
                    finalQueryMock,
                  ]}
                >
                  <Route
                    component={GroupScopeView}
                    path={"/orgs/:organizationName/groups/:groupName/scope"}
                  />
                </MockedProvider>
              </MemoryRouter>
            </groupContext.Provider>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("button", { name: "group.scope.common.add" })
      ).toHaveLength(1);
    });

    await userEvent.hover(
      screen.queryAllByRole("button", { name: "group.scope.common.add" })[0]
    );

    await userEvent.click(
      screen.getByText("components.repositoriesDropdown.manual.text")
    );

    expect(screen.queryByRole("textbox", { name: "url" })).toBeInTheDocument();
    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "https://gitlab.com/fluidattacks/universe"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "branch" }),
      "master"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "production"
    );

    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.token" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();

    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).toHaveValue("USER");

    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).toBeInTheDocument();

    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.name" }),
      "credential name"
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.user" }),
      "user-test"
    );

    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.password" }),
      "password-test"
    );

    await userEvent.click(screen.getByRole("radio", { name: "No" }));
    const numberOfRejectionCheckbox: number = 4;

    expect(screen.queryAllByRole("checkbox", { checked: false })).toHaveLength(
      numberOfRejectionCheckbox
    );

    await userEvent.click(screen.getByDisplayValue("rejectA"));
    await userEvent.click(screen.getByDisplayValue("rejectB"));
    await userEvent.click(screen.getByDisplayValue("rejectC"));

    expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
      numberOfRejectionCheckbox - 1
    );

    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HealthCheck
          "group.scope.git.healthCheck.no",
        ].join("")
      );
    });
  });

  it("should add git roots with ssh credentials", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
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
    const mutationMock: MockedResponse = {
      request: {
        query: ADD_GIT_ROOT,
        variables: {
          branch: "master",
          credentials: {
            azureOrganization: undefined,
            isPat: false,
            key: "LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KdGVzdAotLS0tLUVORCBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0=",
            name: "credential name",
            password: "",
            token: "",
            type: "SSH",
            user: "",
          },
          environment: "production",
          gitignore: [],
          groupName: "unittesting",
          includesHealthCheck: false,
          nickname: "",
          url: "git@gitlab.com:fluidattacks/universe.git",
          useVpn: false,
        },
      },
      result: {
        data: { addGitRoot: { __typename: "SimplePayload", success: true } },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "ACTIVE",
                url: "ssh://git@gitlab.com:fluidattacks/universe.git",
                useVpn: false,
              },
            ],
          },
        },
      },
    };

    jest.clearAllMocks();

    render(
      <authContext.Provider
        value={{
          setUser: jest.fn(),
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_service_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_add_secret_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <groupContext.Provider
              value={{
                organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
                path: "",
                url: "",
              }}
            >
              <MemoryRouter
                initialEntries={["/orgs/okada/groups/unittesting/scope"]}
              >
                <MockedProvider
                  cache={getCache()}
                  mocks={[
                    ...mocks,
                    initialQueryMock,
                    mutationMock,
                    finalQueryMock,
                  ]}
                >
                  <Route
                    component={GroupScopeView}
                    path={"/orgs/:organizationName/groups/:groupName/scope"}
                  />
                </MockedProvider>
              </MemoryRouter>
            </groupContext.Provider>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("button", { name: "group.scope.common.add" })
      ).toHaveLength(1);
    });

    await userEvent.hover(
      screen.queryAllByRole("button", { name: "group.scope.common.add" })[0]
    );

    await userEvent.click(
      screen.getByText("components.repositoriesDropdown.manual.text")
    );

    expect(screen.queryByRole("textbox", { name: "url" })).toBeInTheDocument();
    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "git@gitlab.com:fluidattacks/universe.git"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "branch" }),
      "master"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "production"
    );

    expect(
      screen.getByRole("combobox", { name: "credentials.typeCredential" })
    ).toHaveValue("SSH");

    expect(
      screen.queryByRole("textbox", { name: "credentials.key" })
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.password" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.user" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.token" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "credentials.azureOrganization" })
    ).not.toBeInTheDocument();

    await userEvent.clear(
      screen.getByRole("textbox", { name: "credentials.name" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.name" }),
      "credential name"
    );
    await userEvent.clear(
      screen.getByRole("textbox", { name: "credentials.key" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "credentials.key" }),
      "-----BEGIN OPENSSH PRIVATE KEY-----\ntest\n-----END OPENSSH PRIVATE KEY-----"
    );

    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "ssh://git@gitlab.com:fluidattacks/universe.git",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HealthCheck
          "group.scope.git.healthCheck.no",
        ].join("")
      );
    });
  });

  it("should update git roots", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                gitignore: ["bower_components/*"],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
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
    };
    const mutationMock: MockedResponse = {
      request: {
        query: UPDATE_GIT_ROOT,
        variables: {
          branch: "master",
          credentials: undefined,
          environment: "staging",
          gitignore: ["node_modules/*"],
          groupName: "unittesting",
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
          includesHealthCheck: true,
          nickname: "",
          url: "https://gitlab.com/fluidattacks/universe",
          useVpn: false,
        },
      },
      result: {
        data: { updateGitRoot: { __typename: "SimplePayload", success: true } },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                environment: "staging",
                gitEnvironmentUrls: [],
                gitignore: ["node_modules/*"],
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
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={
            new PureAbility([
              { action: "has_service_white" },
              { action: "has_squad" },
            ])
          }
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
                { action: "update_git_root_filter" },
              ])
            }
          >
            <groupContext.Provider
              value={{
                organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
                path: "",
                url: "",
              }}
            >
              <MemoryRouter
                initialEntries={["/orgs/okada/groups/unittesting/scope"]}
              >
                <MockedProvider
                  cache={getCache()}
                  mocks={[
                    ...mocks,
                    initialQueryMock,
                    mutationMock,
                    finalQueryMock,
                  ]}
                >
                  <Route
                    component={GroupScopeView}
                    path={"/orgs/:organizationName/groups/:groupName/scope"}
                  />
                </MockedProvider>
              </MemoryRouter>
            </groupContext.Provider>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("table")[0]).queryByText(
          "table.noDataIndication"
        )
      ).not.toBeInTheDocument();
    });

    expect(
      within(screen.queryAllByRole("table")[0]).queryAllByRole("row")
    ).toHaveLength(2);

    await userEvent.click(screen.queryAllByRole("row")[1]);
    await waitFor((): void => {
      expect(screen.getByText("group.scope.common.edit")).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.clear(screen.getByRole("textbox", { name: "environment" }));
    await userEvent.type(
      screen.getByRole("textbox", { name: "environment" }),
      "staging"
    );
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("radio", { checked: true, name: "Yes" })
      ).toHaveLength(1);
    });
    await userEvent.clear(
      screen.getByRole("textbox", { name: "gitignore[0]" })
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "gitignore[0]" }),
      "node_modules/*"
    );
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("radio", { checked: true, name: "No" })
      ).toHaveLength(1);
    });
    await userEvent.click(screen.getAllByRole("radio", { name: "Yes" })[1]);
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("radio", { checked: true, name: "Yes" })
      ).toHaveLength(2);
    });
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("radio", { checked: true, name: "No" })
      ).toHaveLength(0);
    });
    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { checked: false })
      ).toHaveLength(2);
    });
    await userEvent.click(screen.getByDisplayValue("includeA"));
    await waitFor((): void => {
      expect(screen.queryAllByRole("checkbox", { checked: true })).toHaveLength(
        1
      );
    });
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")[1].textContent).toStrictEqual(
        [
          // Url
          "https://gitlab.com/fluidattacks/universe",
          // Branch
          "master",
          // State
          "Active",
          // Cloning status
          "Unknown",
          // HeathCheck
          "group.scope.git.healthCheck.yes",
        ].join("")
      );
    });
  });

  it("should activate root", async (): Promise<void> => {
    expect.hasAssertions();

    const initialQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
                lastEditedAt: "2022-10-21T15:58:31+00:00",
                lastEditedBy: "testuser2@test.test",
                nickname: "universe",
                state: "INACTIVE",
                url: "https://gitlab.com/fluidattacks/universe",
                useVpn: false,
              },
            ],
          },
        },
      },
    };
    const mutationMock: MockedResponse = {
      request: {
        query: ACTIVATE_ROOT,
        variables: {
          groupName: "unittesting",
          id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
        },
      },
      result: {
        data: {
          activateRoot: { __typename: "SimplePayload", success: true },
        },
      },
    };
    const finalQueryMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
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
                gitignore: [],
                id: "ROOT#4039d098-ffc5-4984-8ed3-eb17bca98e19",
                includesHealthCheck: false,
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
    };

    render(
      <authContext.Provider
        value={{
          tours: {
            newGroup: true,
            newRiskExposure: true,
            newRoot: true,
            welcome: true,
          },
          userEmail: "",
          userName: "",
        }}
      >
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "has_service_white" }])}
        >
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_activate_root_mutate" },
              ])
            }
          >
            <groupContext.Provider
              value={{
                organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
                path: "",
                url: "",
              }}
            >
              <MemoryRouter
                initialEntries={["/orgs/okada/groups/unittesting/scope"]}
              >
                <MockedProvider
                  cache={getCache()}
                  mocks={[
                    ...mocks,
                    initialQueryMock,
                    mutationMock,
                    finalQueryMock,
                  ]}
                >
                  <Route
                    component={GroupScopeView}
                    path={"/orgs/:organizationName/groups/:groupName/scope"}
                  />
                </MockedProvider>
              </MemoryRouter>
            </groupContext.Provider>
          </authzPermissionsContext.Provider>
        </authzGroupContext.Provider>
      </authContext.Provider>
    );

    await waitFor((): void => {
      expect(
        within(screen.queryAllByRole("table")[0]).queryByText(
          "table.noDataIndication"
        )
      ).not.toBeInTheDocument();
    });

    expect(
      within(screen.queryAllByRole("table")[0]).queryAllByRole("row")
    ).toHaveLength(2);
    expect(
      screen.queryByText("group.scope.common.confirm")
    ).not.toBeInTheDocument();
    expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(false);

    await userEvent.click(screen.getByRole("checkbox"));
    await waitFor((): void => {
      expect(
        screen.queryByText("group.scope.common.confirm")
      ).toBeInTheDocument();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(true);
    });
  });

  it.each(["REGISTERED_BY_MISTAKE"])(
    "should deactivate root with reason %s",
    async (reason): Promise<void> => {
      expect.hasAssertions();

      const initialQueryMock: MockedResponse = {
        request: {
          query: GET_ROOTS,
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
                  gitignore: [],
                  id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
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
      };
      const mutationMock: MockedResponse = {
        request: {
          query: DEACTIVATE_ROOT,
          variables: {
            groupName: "unittesting",
            id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
            other: "",
            reason,
          },
        },
        result: {
          data: {
            deactivateRoot: { __typename: "SimplePayload", success: true },
          },
        },
      };
      const finalQueryMock: MockedResponse = {
        request: {
          query: GET_ROOTS,
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
                  gitignore: [],
                  id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
                  includesHealthCheck: false,
                  lastEditedAt: "2022-10-21T15:58:31+00:00",
                  lastEditedBy: "testuser2@test.test",
                  nickname: "universe",
                  state: "INACTIVE",
                  url: "https://gitlab.com/fluidattacks/universe",
                  useVpn: false,
                },
              ],
            },
          },
        },
      };
      const meGoupAndRootVulnsQueryMock: MockedResponse[] = [
        {
          request: {
            query: GET_GROUPS,
            variables: {},
          },
          result: {
            data: {
              me: {
                __typename: "Me",
                organizations: [
                  {
                    __typename: "Organization",
                    groups: [
                      {
                        __typename: "Group",
                        name: "unittesting",
                        organization: "okada",
                        service: "WHITE",
                      },
                    ],
                    name: "okada",
                  },
                ],
                userEmail: "",
              },
            },
          },
        },
        {
          request: {
            query: GET_ROOTS_VULNS,
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
                    vulnerabilities: [],
                  },
                ],
              },
            },
          },
        },
      ];

      render(
        <authContext.Provider
          value={{
            tours: {
              newGroup: true,
              newRiskExposure: true,
              newRoot: true,
              welcome: true,
            },
            userEmail: "",
            userName: "",
          }}
        >
          <authzGroupContext.Provider
            value={
              new PureAbility([
                { action: "has_service_white" },
                { action: "has_squad" },
              ])
            }
          >
            <authzPermissionsContext.Provider
              value={
                new PureAbility([
                  { action: "api_mutations_activate_root_mutate" },
                ])
              }
            >
              <groupContext.Provider
                value={{
                  organizationId: "f0c74b3e-bce4-4946-ba63-cb7e113ee817",
                  path: "",
                  url: "",
                }}
              >
                <MemoryRouter
                  initialEntries={["/orgs/okada/groups/unittesting/scope"]}
                >
                  <MockedProvider
                    cache={getCache()}
                    mocks={[
                      ...mocks,
                      initialQueryMock,
                      ...meGoupAndRootVulnsQueryMock,
                      mutationMock,
                      finalQueryMock,
                    ]}
                  >
                    <Route
                      component={GroupScopeView}
                      path={"/orgs/:organizationName/groups/:groupName/scope"}
                    />
                  </MockedProvider>
                </MemoryRouter>
              </groupContext.Provider>
            </authzPermissionsContext.Provider>
          </authzGroupContext.Provider>
        </authContext.Provider>
      );

      await waitFor((): void => {
        expect(
          within(screen.queryAllByRole("table")[0]).queryByText(
            "table.noDataIndication"
          )
        ).not.toBeInTheDocument();
      });

      expect(
        within(screen.queryAllByRole("table")[0]).queryAllByRole("row")
      ).toHaveLength(2);
      expect(
        screen.queryByText("group.scope.common.confirm")
      ).not.toBeInTheDocument();
      expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(true);

      await userEvent.click(screen.getByRole("checkbox"));
      await waitFor((): void => {
        expect(
          screen.queryAllByText("group.scope.common.deactivation.title")
        ).toHaveLength(1);
      });

      expect(screen.getByText(btnConfirm)).toBeDisabled();

      await userEvent.selectOptions(
        screen.getByRole("combobox", { name: "reason" }),
        [reason]
      );
      await waitFor((): void => {
        expect(screen.getByText(btnConfirm)).not.toBeDisabled();
      });

      expect(
        screen.queryByText("group.scope.common.confirm")
      ).not.toBeInTheDocument();

      await userEvent.click(screen.getByText(btnConfirm));
      await waitFor((): void => {
        expect(
          screen.queryByText("group.scope.common.confirm")
        ).toBeInTheDocument();
      });
      await userEvent.click(screen.getAllByText(btnConfirm)[1]);

      await waitFor((): void => {
        expect(screen.getByRole<HTMLInputElement>("checkbox").checked).toBe(
          false
        );
      });
    }
  );
});
