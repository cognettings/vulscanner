import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import type { IGetFilesQuery } from "./types";

import { GroupSettingsView } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView";
import {
  GET_FILES,
  GET_GROUP_ACCESS_INFO,
  GET_GROUP_DATA,
  GET_TAGS,
} from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import { GET_GROUP_POLICIES } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/Group/queries";
import { getCache } from "utils/apollo";
import { msgError } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgError").mockImplementation();

    return mockedNotifications;
  }
);

describe("GroupSettingsView", (): void => {
  const mockedQueries: readonly MockedResponse[] = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "TEST",
            tags: ["test"],
          },
        },
      },
    },
    {
      request: {
        query: GET_FILES,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            __typename: "Resource",
            files: [],
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_DATA,
        variables: {
          groupName: "TEST",
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
            name: "TEST",
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
          groupName: "TEST",
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
            name: "TEST",
            vulnerabilityGracePeriod: null,
          },
        },
      },
    },
    {
      request: {
        query: GET_GROUP_ACCESS_INFO,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            disambiguation: "",
            groupContext: "",
            name: "TEST",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_TAGS,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GroupSettingsView).toBe("function");
  });

  it("should render tags component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    const { container } = render(
      <MockedProvider cache={getCache()} mocks={mockedQueries}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupSettingsView}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(2);
    });

    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(4);
    });

    expect(container.querySelector("#resources")).toBeInTheDocument();
  });

  it("should render a error in component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MockedProvider
        cache={getCache()}
        mocks={[...mockError, ...mockedQueries.slice(1), ...mockError]}
      >
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupSettingsView}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });
    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(1);
    });
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(2);
    });
  });

  it("should render files component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockFiles: MockedResponse<IGetFilesQuery> = {
      request: {
        query: GET_FILES,
        variables: {
          groupName: "TEST",
        },
      },
      result: {
        data: {
          resources: {
            files: [
              {
                description: "shell",
                fileName: "shell.exe",
                uploadDate: "2019-04-24 14:56",
                uploader: "unittest@fluidattacks.com",
              },
              {
                description: "Test",
                fileName: "test.zip",
                uploadDate: "2019-03-01 15:21",
                uploader: "unittest@fluidattacks.com",
              },
            ],
          },
        },
      },
    };

    render(
      <MockedProvider cache={getCache()} mocks={[mockFiles, ...mockedQueries]}>
        <MemoryRouter initialEntries={["/orgs/okada/groups/TEST/scope"]}>
          <Route
            component={GroupSettingsView}
            path={"/orgs/:organizationName/groups/:groupName/scope"}
          />
        </MemoryRouter>
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(2);
    });
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(5);
    });
  });
});
