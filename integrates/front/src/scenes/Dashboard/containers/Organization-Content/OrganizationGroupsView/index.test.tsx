import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { authContext } from "context/auth";
import { authzPermissionsContext } from "context/authz/config";
import { ADD_GROUP_MUTATION } from "scenes/Dashboard/components/AddGroupModal/queries";
import { OrganizationGroups } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView";
import { GET_ORGANIZATION_GROUPS } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView/queries";
import type { IOrganizationGroupsProps } from "scenes/Dashboard/containers/Organization-Content/OrganizationGroupsView/types";
import { msgError } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Organization groups view", (): void => {
  const mockProps: IOrganizationGroupsProps = {
    organizationId: "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof OrganizationGroups).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
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
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "unittesting",
                  openFindings: 2,
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user",
                },
                {
                  description: "One-shot type test group",
                  events: [],
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "oneshottest",
                  openFindings: 1,
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "user_manager",
                },
                {
                  description: "Continuous group for deletion",
                  events: [],
                  hasMachine: true,
                  hasSquad: false,
                  managed: "MANAGED",
                  name: "pendingGroup",
                  openFindings: 2,
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "customer_manager",
                },
              ],
              missedAuthors: 3,
              missedRepositories: 1,
              name: "okada",
              trial: null,
            },
          },
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_group_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={true} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <OrganizationGroups organizationId={mockProps.organizationId} />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });

    expect(screen.getAllByRole("row")).toHaveLength(4);
    expect(
      screen.queryByText("organization.tabs.groups.overview.title.text")
    ).toBeInTheDocument();

    expect(
      screen.queryByText(
        "organization.tabs.groups.overview.coveredAuthors.content"
      )
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "organization.tabs.groups.overview.coveredRepositories.content"
      )
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "organization.tabs.groups.overview.missedAuthors.content"
      )
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "organization.tabs.groups.overview.missedRepositories.content"
      )
    ).toBeInTheDocument();

    const UNIT_TESTING_ROW_AT = 1;

    expect(screen.getAllByRole("button")[1].textContent).toMatch(
      /organization.tabs.groups.newGroup.new.text/u
    );
    expect(screen.getAllByRole("row")[2].textContent).toContain("Oneshottest");
    expect(screen.getAllByRole("row")[2].textContent).toContain(
      "OneshottestSubscribedOneshot1 types foundOne-shot type test groupuserModal.roles.userManagerNone"
    );
    expect(screen.getAllByRole("row")[2].textContent).toContain("Oneshot");
    expect(screen.getAllByRole("row")[2].textContent).toContain(
      "OneshottestSubscribedOneshot1 types foundOne-shot type test groupuserModal.roles.userManagerNone"
    );
    expect(screen.getAllByRole("row")[2].textContent).toContain(
      "One-shot type test group"
    );
    expect(screen.getAllByRole("row")[2].textContent).toContain(
      "userModal.roles.userManager"
    );

    expect(screen.getAllByRole("row")[3].textContent).toContain("Pendinggroup");
    expect(screen.getAllByRole("row")[3].textContent).toContain(
      "PendinggroupSubscribedMachine2 types foundContinuous group for deletionuserModal.roles.customerManagerNone"
    );
    expect(screen.getAllByRole("row")[3].textContent).toContain("Machine");
    expect(screen.getAllByRole("row")[3].textContent).toContain(
      "PendinggroupSubscribedMachine2 types foundContinuous group for deletionuserModal.roles.customerManagerNone"
    );
    expect(screen.getAllByRole("row")[3].textContent).toContain(
      "Continuous group for deletion"
    );
    expect(screen.getAllByRole("row")[3].textContent).toContain(
      "userModal.roles.customerManager"
    );

    expect(
      screen.getAllByRole("row")[UNIT_TESTING_ROW_AT].textContent
    ).toContain("Unittesting");
    expect(
      screen.getAllByRole("row")[UNIT_TESTING_ROW_AT].textContent
    ).toContain("Squad");
    expect(
      screen.getAllByRole("row")[UNIT_TESTING_ROW_AT].textContent
    ).toContain("userModal.roles.user");

    expect(screen.getAllByRole("link")).toHaveLength(13);
    expect(screen.getAllByRole("link")[0]).toHaveAttribute(
      "href",
      "/orgs/okada/outside"
    );

    await userEvent.click(screen.getByRole("cell", { name: "Unittesting" }));
    jest.clearAllMocks();
  });

  it("should show an error", async (): Promise<void> => {
    expect.hasAssertions();

    const mockErrors: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mockErrors}>
          <Route path={"/orgs/:organizationName/groups"}>
            <OrganizationGroups organizationId={mockProps.organizationId} />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    expect(screen.queryAllByRole("table")).toHaveLength(0);

    jest.clearAllMocks();
  });

  it("should add a new group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
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
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "unittesting",
                  openFindings: 1,
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user",
                },
                {
                  description: "One-shot type test group",
                  events: [],
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "oneshottest",
                  openFindings: 2,
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "user_manager",
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
          query: ADD_GROUP_MUTATION,
          variables: {
            description: "Test group",
            groupName: "AKAME",
            hasMachine: true,
            hasSquad: false,
            language: "EN",
            organizationName: "OKADA",
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            addGroup: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_ORGANIZATION_GROUPS,
          variables: {
            organizationId: mockProps.organizationId,
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
                {
                  description: "One-shot type test group",
                  events: [],
                  hasAsm: true,
                  hasForces: false,
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "oneshottest",
                  openFindings: 2,
                  service: "WHITE",
                  subscription: "oneshot",
                  userRole: "user_manager",
                },
                {
                  description: "Test group",
                  events: [],
                  hasAsm: true,
                  hasForces: true,
                  hasMachine: true,
                  hasSquad: true,
                  managed: "MANAGED",
                  name: "akame",
                  openFindings: 1,
                  service: "WHITE",
                  subscription: "continuous",
                  userRole: "user_manager",
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
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_add_group_mutate" },
    ]);

    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
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
                <OrganizationGroups organizationId={mockProps.organizationId} />
              </authContext.Provider>
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    const numberOfRows = 3;
    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });

    expect(screen.getAllByRole("row")).toHaveLength(numberOfRows);

    await userEvent.click(
      screen.getByText("organization.tabs.groups.newGroup.new.text")
    );

    await waitFor((): void => {
      expect(
        screen.getByText("organization.tabs.groups.newGroup.new.group")
      ).toBeInTheDocument();
    });

    expect(screen.getByText("components.modal.confirm")).toBeEnabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "AKAME"
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "description" }),
      "Test group"
    );

    await waitFor((): void => {
      expect(screen.getByText("components.modal.confirm")).not.toBeDisabled();
    });

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor(
      (): void => {
        expect(screen.queryAllByRole("row")).toHaveLength(4);
      },
      { timeout: 2000 }
    );

    jest.clearAllMocks();
  });
});
