import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { authzPermissionsContext } from "context/authz/config";
import { GET_GROUP_DATA as GET_GROUP_SERVICES } from "scenes/Dashboard/containers/Group-Content/GroupRoute/queries";
import {
  GET_GROUP_DATA,
  UPDATE_GROUP_DATA,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import { Services } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services";
import { getCache } from "utils/apollo";
import { msgSuccess } from "utils/notifications";

jest.mock(
  "../../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

    return mockedNotifications;
  }
);

describe("Services", (): void => {
  const btnConfirm = "components.modal.confirm";

  const mockResponses: readonly MockedResponse[] = [
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
            sprintStartDate: "2021-06-06T00:00:00",
            subscription: "CoNtInUoUs",
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
            sprintStartDate: "2021-06-06T00:00:00",
            subscription: "CoNtInUoUs",
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
            sprintStartDate: "2021-06-06T00:00:00",
            subscription: "CoNtInUoUs",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "oneshottest",
        },
      },
      result: {
        data: {
          group: {
            businessId: "",
            businessName: "",
            description: "",
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            managed: "MANAGED",
            name: "oneshottest",
            service: "BLACK",
            sprintDuration: 1,
            sprintStartDate: "2022-06-06T00:00:00",
            subscription: "OnEsHoT",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "not-exists",
        },
      },
      result: {
        data: {
          group: {
            businessId: "",
            businessName: "",
            description: "",
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            managed: "MANAGED",
            name: "not-exists",
            service: "BLACK",
            sprintDuration: 1,
            sprintStartDate: "2022-06-06T00:00:00",
            subscription: "OnEsHoT",
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            organization: "org1",
            serviceAttributes: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            organization: "org1",
            serviceAttributes: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_SERVICES,
        variables: {
          groupName: "unittesting",
        },
      },
      result: {
        data: {
          group: {
            name: "unittesting",
            organization: "org1",
            serviceAttributes: [],
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Services).toBe("function");
  });

  [
    { group: "unittesting", texts: 9 },
    { group: "oneshottest", texts: 10 },
    { group: "not-exists", texts: 0 },
  ].forEach((test: { group: string; texts: number }): void => {
    it(`should render services for: ${test.group}`, async (): Promise<void> => {
      expect.hasAssertions();

      jest.clearAllMocks();

      const mockedPermissions = new PureAbility<string>([
        { action: "api_mutations_update_group_mutate" },
      ]);

      render(
        <MockedProvider cache={getCache()} mocks={mockResponses}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <MemoryRouter initialEntries={["/home"]}>
              <Services groupName={test.group} />
            </MemoryRouter>
          </authzPermissionsContext.Provider>
        </MockedProvider>
      );

      await waitFor((): void => {
        expect(
          screen.queryAllByText("searchFindings.servicesTable.", {
            exact: false,
          })
        ).toHaveLength(test.texts);
      });

      await waitFor((): void => {
        expect(screen.getByLabelText("type")).not.toBeDisabled();
      });

      expect(screen.getByLabelText("service")).not.toBeDisabled();
      expect(
        screen.getByRole("checkbox", { name: "machine" })
      ).not.toBeDisabled();
      expect(
        screen.getByRole("checkbox", { name: "squad" })
      ).not.toBeDisabled();
    });
  });

  it("should toggle buttons properly", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockMutations: readonly MockedResponse[] = [
      {
        request: {
          query: UPDATE_GROUP_DATA,
          variables: {
            comments: "",
            description: "Integrates unit test project",
            groupName: "unittesting",
            hasASM: true,
            hasMachine: true,
            hasSquad: true,
            language: "EN",
            reason: "NONE",
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            updateGroup: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_GROUP_DATA,
          variables: {
            comments: "",
            description: "Integrates unit test project",
            groupName: "unittesting",
            hasASM: true,
            hasMachine: false,
            hasSquad: false,
            language: "EN",
            reason: "NONE",
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            updateGroup: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_GROUP_DATA,
          variables: {
            comments: "",
            description: "Integrates unit test project",
            groupName: "unittesting",
            hasASM: true,
            hasMachine: true,
            hasSquad: false,
            language: "EN",
            reason: "NONE",
            service: "WHITE",
            subscription: "CONTINUOUS",
          },
        },
        result: {
          data: {
            updateGroup: {
              success: true,
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
              businessId: "",
              businessName: "",
              description: "Integrates unit test project",
              hasASM: true,
              hasMachine: true,
              hasSquad: false,
              language: "EN",
              managed: "MANAGED",
              name: "unittesting",
              service: "WHITE",
              sprintDuration: "1",
              sprintStartDate: "2021-06-06T00:00:00",
              subscription: "CONTINUOUS",
            },
          },
        },
      },
    ];

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_group_mutate" },
    ]);

    render(
      <MockedProvider
        cache={getCache()}
        mocks={[...mockResponses, ...mockMutations]}
      >
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MemoryRouter initialEntries={["/home"]}>
            <Services groupName={"unittesting"} />
          </MemoryRouter>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByText("searchFindings.servicesTable.", { exact: false })
      ).toHaveLength(9);
    });

    await userEvent.click(screen.getByRole("checkbox", { name: "machine" }));

    await waitFor((): void => {
      expect(
        screen.getByText("searchFindings.servicesTable.modal.continue")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.modal.continue")
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.type(
      screen.getByPlaceholderText("unittesting"),
      "unittesting"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.servicesTable.success",
        "searchFindings.servicesTable.successTitle"
      );
    });

    await userEvent.click(screen.getByRole("checkbox", { name: "squad" }));
    await waitFor((): void => {
      expect(
        screen.getByText("searchFindings.servicesTable.modal.continue")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.modal.continue")
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.clear(screen.getByPlaceholderText("unittesting"));
    await userEvent.type(
      screen.getByPlaceholderText("unittesting"),
      "unittesting"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.servicesTable.success",
        "searchFindings.servicesTable.successTitle"
      );
    });

    await userEvent.click(screen.getByRole("checkbox", { name: "squad" }));
    await waitFor((): void => {
      expect(
        screen.getByText("searchFindings.servicesTable.modal.continue")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("searchFindings.servicesTable.modal.continue")
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).toBeInTheDocument();
    });
    await userEvent.clear(screen.getByPlaceholderText("unittesting"));
    await userEvent.type(
      screen.getByPlaceholderText("unittesting"),
      "unittesting"
    );
    await waitFor((): void => {
      expect(screen.getByText(btnConfirm)).not.toBeDisabled();
    });
    await userEvent.click(screen.getByText(btnConfirm));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.servicesTable.success",
        "searchFindings.servicesTable.successTitle"
      );
    });
    await waitFor((): void => {
      expect(screen.queryByRole("button")).not.toBeInTheDocument();
    });
    await waitFor((): void => {
      expect(screen.getByRole("combobox", { name: "type" })).toHaveValue(
        "CONTINUOUS"
      );
    });

    expect(screen.getByRole("combobox", { name: "service" })).toHaveValue(
      "WHITE"
    );
    expect(
      screen.getAllByText("searchFindings.servicesTable.inactive")
    ).toHaveLength(1);
    expect(
      screen.getAllByText("searchFindings.servicesTable.active")
    ).toHaveLength(1);
  });

  it("should display services form as read-only", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const mockMutations: readonly MockedResponse[] = [
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
              businessId: "",
              businessName: "",
              description: "Integrates unit test project",
              hasASM: true,
              hasMachine: true,
              hasSquad: false,
              language: "EN",
              managed: "MANAGED",
              name: "unittesting",
              service: "WHITE",
              sprintDuration: "1",
              sprintStartDate: "2022-05-06T00:00:00",
              subscription: "CONTINUOUS",
            },
          },
        },
      },
    ];
    const mockedPermissions = new PureAbility<string>([
      { action: "see_group_services_info" },
    ]);
    render(
      <MockedProvider cache={getCache()} mocks={...mockMutations}>
        <authzPermissionsContext.Provider value={mockedPermissions}>
          <MemoryRouter initialEntries={["/home"]}>
            <Services groupName={"unittesting"} />
          </MemoryRouter>
        </authzPermissionsContext.Provider>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.queryAllByText("searchFindings.servicesTable.", { exact: false })
      ).toHaveLength(9);
    });

    expect(screen.getByLabelText("type")).toBeDisabled();
    expect(screen.getByLabelText("service")).toBeDisabled();
    expect(screen.getByRole("checkbox", { name: "machine" })).toBeDisabled();
    expect(screen.getByRole("checkbox", { name: "squad" })).toBeDisabled();
  });
});
