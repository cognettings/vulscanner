import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_GROUP_SERVICES } from "hooks/queries";
import { Breadcrumb } from "pages/home/dashboard/navbar/breadcrumb";
import {
  GET_ORGANIZATION_GROUP_NAMES,
  GET_USER_ORGANIZATIONS,
  GET_USER_TAGS,
} from "pages/home/dashboard/navbar/breadcrumb/queries";
import { GET_ME_VULNERABILITIES_ASSIGNED_IDS } from "pages/home/dashboard/navbar/to-do/queries";
import { Unsubscribe } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Unsubscribe";
import { UNSUBSCRIBE_FROM_GROUP_MUTATION } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Unsubscribe/UnsubscribeModal/queries";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { GET_USER_ORGANIZATIONS_GROUPS } from "scenes/Dashboard/queries";
import { getCache } from "utils/apollo";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Unsubscribe from group", (): void => {
  const btnConfirm = "components.modal.confirm";
  const mockedQuery: MockedResponse[] = [
    {
      request: {
        query: GET_ME_VULNERABILITIES_ASSIGNED_IDS,
        variables: {},
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            userEmail: "test@test.test",
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
            userEmail: "test@test.test",
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
            __type: "Organization",
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
            userEmail: "test@test.test",
          },
        },
      },
    },
    {
      request: {
        query: GET_USER_ORGANIZATIONS_GROUPS,
        variables: {},
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            organizations: [
              {
                groups: [
                  {
                    name: "test",
                    permissions: [],
                    serviceAttributes: [],
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
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Unsubscribe).toBe("function");
  });

  it("should unsubscribe from a group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: GET_GROUP_SERVICES,
          variables: {
            groupName: "test",
          },
        },
        result: {
          data: {
            group: {
              __typename: "Group",
              name: "test",
              serviceAttributes: [],
            },
          },
        },
      },
      {
        request: {
          query: UNSUBSCRIBE_FROM_GROUP_MUTATION,
          variables: {
            groupName: "test",
          },
        },
        result: { data: { unsubscribeFromGroup: { success: true } } },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/orgs/okada/groups/test/scope"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[...mockedQuery, ...mocksMutation, ...mockedQuery]}
        >
          <Route path={"/orgs/:organizationName/groups/:groupName/scope"}>
            <Breadcrumb />
            <Unsubscribe />
          </Route>
        </MockedProvider>
      </MemoryRouter>
    );

    expect(
      screen.queryByText("searchFindings.servicesTable.unsubscribe.button")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.unsubscribe.button")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "confirmation" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "confirmation" }),
      "test"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.servicesTable.unsubscribe.success",
        "searchFindings.servicesTable.unsubscribe.successTitle"
      );
    });
  });

  it("shouldn't unsubscribe from a group", async (): Promise<void> => {
    expect.hasAssertions();

    const mocksMutation: MockedResponse[] = [
      {
        request: {
          query: UNSUBSCRIBE_FROM_GROUP_MUTATION,
          variables: {
            groupName: "test",
          },
        },
        result: {
          errors: [new GraphQLError("Access denied")],
        },
      },
    ];
    render(
      <MemoryRouter initialEntries={["/test"]}>
        <MockedProvider addTypename={true} mocks={mocksMutation}>
          <Route component={Unsubscribe} path={"/:groupName"} />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(
      screen.queryByText("searchFindings.servicesTable.unsubscribe.button")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.unsubscribe.button")
    );
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "confirmation" })
      ).toBeInTheDocument();
    });

    expect(screen.getByText(btnConfirm)).toBeDisabled();

    await userEvent.type(
      screen.getByRole("textbox", { name: "confirmation" }),
      "test"
    );
    await userEvent.click(screen.getByText(btnConfirm));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
  });
});
