/* eslint-disable react/jsx-props-no-spreading
  --------
  Best way to pass down props for test wrappers.
*/
import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { act } from "react-dom/test-utils";

import {
  GET_GROUP_BILLING,
  GET_ORGANIZATION_BILLING,
} from "./confirm-invitation/queries";

import { authzPermissionsContext } from "context/authz/config";
import { AddUserModal } from "features/add-user-modal";
import { GET_STAKEHOLDER } from "features/add-user-modal/queries";
import type { IAddStakeholderModalProps } from "features/add-user-modal/types";
import { getCache } from "utils/apollo";
import { msgError } from "utils/notifications";

jest.mock("utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

const functionMock = jest.fn();

describe("Add user modal", (): void => {
  const mockPropsAdd: IAddStakeholderModalProps = {
    action: "add",
    domainSuggestions: [],
    editTitle: "",
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    suggestions: [],
    title: "",
    type: "user",
  };

  const mockPropsEdit: IAddStakeholderModalProps = {
    action: "edit",
    domainSuggestions: [],
    editTitle: "edit title",
    initialValues: {
      email: "user@test.com",
      role: "USER",
    },
    onClose: functionMock,
    onSubmit: functionMock,
    open: true,
    suggestions: [],
    title: "",
    type: "user",
  };

  const mocks: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_BILLING,
        variables: { groupName: "TEST" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            billing: {
              __typename: "Billing",
              authors: [{ actor: "Test <test@test.com>" }],
            },
            name: "TEST",
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "user@test.com",
        },
      },
      result: {
        data: {
          stakeholder: {
            __typename: "Stakeholder",
            email: "user@test.com",
            responsibility: "tester",
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        data: {
          stakeholder: {
            __typename: "Stakeholder",
            email: "unittest@test.com",
            responsibility: "edited",
          },
        },
      },
    },
  ];

  const mockError: MockedResponse[] = [
    {
      request: {
        query: GET_GROUP_BILLING,
        variables: { groupName: "TEST" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            billing: {
              __typename: "Billing",
              authors: [{ actor: "Test <test@test.com>" }],
            },
            name: "TEST",
          },
        },
      },
    },
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "user@test.com",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
    {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "unittest@test.com",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddUserModal).toBe("function");
  });

  it("should handle errors when auto fill data", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider cache={getCache()} mocks={mockError}>
        <AddUserModal {...mockPropsEdit} groupName={"TEST"} type={"group"} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("user@test.com");
    });

    expect(screen.queryByText("edit title")).toBeInTheDocument();

    fireEvent.blur(screen.getByPlaceholderText("userModal.emailPlaceholder"));
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });

  it("should render an add component group", async (): Promise<void> => {
    expect.hasAssertions();

    const mockUser = {
      request: {
        query: GET_STAKEHOLDER,
        variables: {
          entity: "GROUP",
          groupName: "TEST",
          organizationId: "-",
          userEmail: "user@test.com",
        },
      },
      result: {
        data: {
          stakeholder: null,
        },
        errors: [new GraphQLError("Access denied or stakeholder not found")],
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "grant_group_level_role:user" },
    ]);

    render(
      <MockedProvider cache={getCache()} mocks={[mocks[0], mockUser]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <AddUserModal {...mockPropsAdd} groupName={"TEST"} type={"group"} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("");
    });

    fireEvent.change(screen.getByRole("combobox", { name: "email" }), {
      target: { value: "user@test.com" },
    });
    act((): void => {
      fireEvent.blur(screen.getByRole("combobox", { name: "email" }));
    });

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledTimes(0);
    });

    expect(screen.queryByText("Required field")).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "role" }),
      ["USER"]
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    expect(screen.queryByText("Required field")).toBeInTheDocument();

    expect(screen.queryByText("Confirm invitation")).not.toBeInTheDocument();

    await userEvent.type(
      screen.getByRole("textbox", { name: "responsibility" }),
      "Group Tester"
    );

    expect(screen.queryByText("Required field")).not.toBeInTheDocument();

    await userEvent.click(screen.getByText("components.modal.confirm"));
    await waitFor((): void => {
      expect(screen.queryByText("Confirm invitation")).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render an add component organization", async (): Promise<void> => {
    expect.hasAssertions();

    const mockOrganization = {
      request: {
        query: GET_ORGANIZATION_BILLING,
        variables: {
          organizationId: "ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817",
        },
      },
      result: {
        data: {
          organization: {
            __typename: "Organization",
            billing: { authors: [] },
            name: "okada",
          },
        },
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "grant_organization_level_role:user" },
    ]);

    render(
      <MockedProvider cache={getCache()} mocks={[mockOrganization]}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <AddUserModal
            {...mockPropsAdd}
            organizationId={"ORG#f0c74b3e-bce4-4946-ba63-cb7e113ee817"}
            type={"organization"}
          />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("");
    });

    fireEvent.change(screen.getByRole("combobox", { name: "email" }), {
      target: { value: "user@test.com" },
    });
    act((): void => {
      fireEvent.blur(screen.getByRole("combobox", { name: "email" }));
    });

    expect(screen.queryByText("Required field")).not.toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "role" }),
      ["USER"]
    );
    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(screen.queryByText("Confirm invitation")).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render an edit component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider cache={getCache()} mocks={mocks}>
        <AddUserModal {...mockPropsEdit} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("user@test.com");
    });
    jest.clearAllMocks();
  });

  it("should auto fill data on inputs", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MockedProvider cache={getCache()} mocks={mocks}>
        <AddUserModal {...mockPropsAdd} groupName={"TEST"} type={"group"} />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(
        screen.getByPlaceholderText("userModal.emailPlaceholder")
      ).toHaveValue("");
    });
    fireEvent.change(screen.getByRole("combobox", { name: "email" }), {
      target: { value: "unittest@test.com" },
    });
    act((): void => {
      fireEvent.blur(screen.getByRole("combobox", { name: "email" }));
    });
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "responsibility" })
      ).toHaveValue("edited");
    });
    jest.clearAllMocks();
  });

  it("should render user level role options", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "grant_user_level_role:admin" },
      { action: "grant_user_level_role:user" },
      { action: "grant_user_level_role:hacker" },
    ]);
    render(
      <MockedProvider cache={getCache()} mocks={mocks}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <AddUserModal {...mockPropsAdd} groupName={undefined} />
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("combobox")).toHaveLength(2);
    });

    expect(screen.queryAllByRole("option")).toHaveLength(4);
    expect(
      screen.getByRole("option", {
        name: "userModal.roles.admin",
        selected: false,
      })
    ).toHaveValue("ADMIN");
    expect(
      screen.getByRole("option", {
        name: "userModal.roles.hacker",
        selected: false,
      })
    ).toHaveValue("HACKER");
    expect(
      screen.getByRole("option", {
        name: "userModal.roles.user",
        selected: false,
      })
    ).toHaveValue("USER");
    expect(
      screen.getByRole("option", { name: "", selected: true })
    ).toHaveValue("");

    jest.clearAllMocks();
  });
});
