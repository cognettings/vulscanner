import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { authzPermissionsContext } from "context/authz/config";
import { GroupPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Group";
import {
  GET_GROUP_POLICIES,
  UPDATE_GROUP_POLICIES,
} from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Group/queries";
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

describe("Group policies view", (): void => {
  const groupPolicyFields: number = 6;
  const mockedPermissions = new PureAbility<string>([
    { action: "api_mutations_update_group_policies_mutate" },
  ]);

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof GroupPolicies).toBe("function");
  });

  it("should render with default values", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              maxAcceptanceDays: null,
              maxAcceptanceSeverity: 10,
              maxNumberAcceptances: null,
              minAcceptanceSeverity: 0,
              minBreakingSeverity: 0,
              name: "unittesting",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
        <MockedProvider cache={getCache()} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={GroupPolicies}
              path={"/orgs/:organizationName/groups/:groupName/scope"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(groupPolicyFields);
    });

    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    ).toHaveValue("");
    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceSeverity" })
    ).toHaveValue("10.0");
    expect(
      screen.getByRole("textbox", { name: "maxNumberAcceptances" })
    ).toHaveValue("");
    expect(
      screen.getByRole("textbox", { name: "minAcceptanceSeverity" })
    ).toHaveValue("0.0");
    expect(
      screen.getByRole("textbox", { name: "minBreakingSeverity" })
    ).toHaveValue("0.0");
    expect(
      screen.getByRole("textbox", { name: "vulnerabilityGracePeriod" })
    ).toHaveValue("1");
  });

  it("should render an error message", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_POLICIES,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          errors: [new GraphQLError("An error occurred")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
        <MockedProvider cache={getCache()} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups/:groupName/scope"}>
            <GroupPolicies />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(1);
    });

    expect(screen.queryAllByRole("table")).toHaveLength(0);
  });

  it("should update the policies", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptances: 5,
              minAcceptanceSeverity: 3,
              minBreakingSeverity: 1,
              name: "unittesting",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_GROUP_POLICIES,
          variables: {
            groupName: "unittesting",
            maxAcceptanceDays: 2,
            maxAcceptanceSeverity: 8.9,
            maxNumberAcceptances: 1,
            minAcceptanceSeverity: 0,
            minBreakingSeverity: 4,
            vulnerabilityGracePeriod: 2,
          },
        },
        result: {
          data: {
            updateGroupPolicies: {
              success: true,
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
              findingPolicies: [],
              inactivityPeriod: 180,
              maxAcceptanceDays: 2,
              maxAcceptanceSeverity: 8.9,
              maxNumberAcceptances: 1,
              minAcceptanceSeverity: 0,
              minBreakingSeverity: 4,
              name: "okada",
              vulnerabilityGracePeriod: 2,
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
        <MockedProvider cache={getCache()} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups/:groupName/scope"}>
            <authzPermissionsContext.Provider value={mockedPermissions}>
              <GroupPolicies />
            </authzPermissionsContext.Provider>
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(groupPolicyFields);
    });

    expect(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" })
    ).toHaveValue("5");
    expect(
      screen.queryByText("organization.tabs.policies.save")
    ).not.toBeInTheDocument();

    await userEvent.clear(screen.getAllByRole("textbox")[0]);
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxAcceptanceDays" }),
      "2"
    );
    await userEvent.clear(screen.getAllByRole("textbox")[1]);
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxNumberAcceptances" }),
      "1"
    );
    await userEvent.clear(screen.getAllByRole("textbox")[2]);
    await userEvent.type(
      screen.getByRole("textbox", { name: "vulnerabilityGracePeriod" }),
      "2"
    );
    await userEvent.clear(screen.getAllByRole("textbox")[3]);
    await userEvent.type(
      screen.getByRole("textbox", { name: "minAcceptanceSeverity" }),
      "0"
    );
    await userEvent.clear(screen.getAllByRole("textbox")[4]);
    await userEvent.type(
      screen.getByRole("textbox", { name: "maxAcceptanceSeverity" }),
      "8.9"
    );
    await userEvent.clear(screen.getAllByRole("textbox")[5]);
    await userEvent.type(
      screen.getByRole("textbox", { name: "minBreakingSeverity" }),
      "4"
    );

    await waitFor((): void => {
      expect(
        screen.queryByText("organization.tabs.policies.save")
      ).toBeInTheDocument();
    });

    await userEvent.click(screen.getByText("organization.tabs.policies.save"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledTimes(1);
    });

    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "maxAcceptanceDays" })
      ).toHaveValue("2");
    });

    expect(
      screen.queryByRole("textbox", { name: "inactivityPeriod" })
    ).not.toBeInTheDocument();
  });

  it("should not show save button", async (): Promise<void> => {
    expect.hasAssertions();

    const mocks: readonly MockedResponse[] = [
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
              maxAcceptanceDays: 5,
              maxAcceptanceSeverity: 7.5,
              maxNumberAcceptances: 2,
              minAcceptanceSeverity: 3,
              minBreakingSeverity: 3,
              name: "unittesting",
              vulnerabilityGracePeriod: 1,
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/unittesting/scope"]}>
        <MockedProvider cache={getCache()} mocks={mocks}>
          <Route path={"/orgs/:organizationName/groups/:groupName/scope"}>
            <GroupPolicies />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("textbox")).toHaveLength(groupPolicyFields);
    });

    expect(
      screen.queryByText("organization.tabs.policies.save")
    ).not.toBeInTheDocument();
  });
});
