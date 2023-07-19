import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { ManagementModal } from "./ManagementModal";
import { AddEnvironment } from "./ManagementModal/Environments/AddEnvironment";
import { GET_FILES } from "./ManagementModal/Environments/AddEnvironment/EnvironmentUrl/queries";

import { GitRoots } from ".";
import { GET_ORGANIZATION_CREDENTIALS as GET_CREDENTIALS_FROM_OAUTH_FORM } from "../../../../components/AddOauthRootForm/queries";
import { GET_ORGANIZATION_CREDENTIALS } from "../queries";
import type { IFormValues, IGitRootAttr } from "../types";
import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { getCache } from "utils/apollo";

describe("GitRoots", (): void => {
  const mockedQueries: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_CREDENTIALS,
      variables: {
        organizationId: "",
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
  };

  const mockedGetCredentialsV2Query: MockedResponse = {
    request: {
      query: GET_CREDENTIALS_FROM_OAUTH_FORM,
      variables: {
        organizationId: "",
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
  };

  const mockedAddFileQuery: MockedResponse = {
    request: {
      query: GET_FILES,
      variables: {
        groupName: "",
      },
    },
    result: {
      data: {
        resources: {
          files: [],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof GitRoots).toBe("function");
  });

  it("should render tables", async (): Promise<void> => {
    expect.hasAssertions();

    const roots: IGitRootAttr[] = [
      {
        __typename: "GitRoot",
        branch: "",
        cloningStatus: {
          message: "",
          status: "UNKNOWN",
        },
        createdAt: new Date("2022-02-10T14:58:10+00:00"),
        createdBy: "testuser1@test.test",
        credentials: {
          auth: "",
          azureOrganization: "",
          id: "",
          isPat: false,
          isToken: false,
          key: "",
          name: "",
          password: "",
          token: "",
          type: "",
          typeCredential: "",
          user: "",
        },
        environment: "",
        gitEnvironmentUrls: [
          {
            cloudName: undefined,
            createdAt: new Date("2022-04-27T17:30:07.230355"),
            createdBy: null,
            id: "3f6eb6274ec7dc2855451c0fbb4ff9485360be5b",
            secrets: [],
            url: "https://app.fluidattacks.com",
            urlType: "URL",
          },
        ],
        gitignore: [],
        healthCheckConfirm: [],
        id: "",
        includesHealthCheck: false,
        lastEditedAt: new Date("2022-10-21T15:58:31+00:00"),
        lastEditedBy: "testuser2@test.test",
        nickname: "",
        secrets: [],
        state: "ACTIVE",
        url: "https://gitlab.com/fluidattacks/universe",
        useVpn: false,
      },
    ];
    const refetch: jest.Mock = jest.fn();
    render(
      <MockedProvider>
        <MemoryRouter initialEntries={["/TEST"]}>
          <GitRoots
            groupName={"unittesting"}
            onUpdate={refetch}
            roots={roots}
          />
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("table")).toHaveLength(2);
    });
  });

  it("should render action buttons", async (): Promise<void> => {
    expect.hasAssertions();

    const refetch: jest.Mock = jest.fn();
    render(
      <MockedProvider
        cache={getCache()}
        mocks={[mockedQueries, mockedGetCredentialsV2Query]}
      >
        <MemoryRouter initialEntries={["/TEST"]}>
          <authzPermissionsContext.Provider
            value={
              new PureAbility([
                { action: "api_mutations_add_git_root_mutate" },
                { action: "api_mutations_update_git_root_mutate" },
              ])
            }
          >
            <GitRoots groupName={"unittesting"} onUpdate={refetch} roots={[]} />
          </authzPermissionsContext.Provider>
        </MemoryRouter>
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("button")).toHaveLength(5);
    });

    await userEvent.hover(
      screen.getByRole("button", { name: "group.scope.common.add" })
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("components.repositoriesDropdown.manual.text")
      ).toBeInTheDocument();
    });
    jest.clearAllMocks();
  });

  it("should render git modal", async (): Promise<void> => {
    expect.hasAssertions();

    const finishTour: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    render(
      <authzGroupContext.Provider
        value={new PureAbility([{ action: "has_squad" }])}
      >
        <authzPermissionsContext.Provider
          value={
            new PureAbility([
              { action: "update_git_root_filter" },
              { action: "api_mutations_add_secret_mutate" },
              { action: "api_mutations_update_git_root_mutate" },
            ])
          }
        >
          <MockedProvider cache={getCache()} mocks={[mockedQueries]}>
            <ManagementModal
              finishTour={finishTour}
              groupName={""}
              initialValues={undefined}
              isEditing={false}
              manyRows={false}
              modalMessages={{ message: "", type: "success" }}
              onClose={handleClose}
              onSubmitRepo={handleSubmit}
              runTour={false}
            />
          </MockedProvider>
        </authzPermissionsContext.Provider>
      </authzGroupContext.Provider>
    );

    // Repository fields
    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "url" })).toBeInTheDocument();
    });

    expect(screen.getByRole("textbox", { name: "branch" })).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "environment" })
    ).toBeInTheDocument();

    // Health Check
    expect(
      screen.queryAllByRole("checkbox", { name: "healthCheckConfirm" })
    ).toHaveLength(0);

    await userEvent.clear(screen.getByRole("textbox", { name: "url" }));
    await userEvent.type(
      screen.getByRole("textbox", { name: "url" }),
      "https://gitlab.com/fluidattacks/universe"
    );

    await userEvent.click(screen.getAllByRole("radio", { name: "Yes" })[1]);

    await waitFor((): void => {
      expect(
        screen.queryAllByRole("checkbox", { name: "healthCheckConfirm" })
      ).toHaveLength(1);
    });

    await userEvent.click(screen.getAllByRole("radio", { name: "Yes" })[0]);

    // Filters
    await waitFor((): void => {
      expect(
        screen.getByRole("textbox", { name: "gitignore[0]" })
      ).toBeInTheDocument();
    });

    jest.clearAllMocks();
  });

  it("should render envs modal", async (): Promise<void> => {
    expect.hasAssertions();

    const finishTour: jest.Mock = jest.fn();
    const handleClose: jest.Mock = jest.fn();
    const handleSubmit: jest.Mock = jest.fn();
    const initialValues: IFormValues = {
      branch: "",
      cloningStatus: {
        message: "",
        status: "UNKNOWN",
      },
      credentials: {
        auth: "",
        azureOrganization: "",
        id: "",
        isPat: false,
        isToken: false,
        key: "",
        name: "",
        password: "",
        token: "",
        type: "",
        typeCredential: "",
        user: "",
      },
      environment: "",
      environmentUrls: [],
      gitEnvironmentUrls: [
        {
          cloudName: undefined,
          createdAt: new Date("2022-04-27T17:30:07.230355"),
          createdBy: "user_test@test.test",
          id: "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
          secrets: [],
          url: "",
          urlType: "URL",
        },
      ],
      gitignore: [],
      hasExclusions: "",
      healthCheckConfirm: [],
      id: "",
      includesHealthCheck: false,
      nickname: "",
      secrets: [],
      state: "ACTIVE",
      url: "https://gitlab.com/fluidattacks/universe",
      useVpn: false,
    };
    render(
      <authzPermissionsContext.Provider
        value={
          new PureAbility([
            { action: "api_mutations_update_git_environments_mutate" },
            { action: "api_mutations_add_secret_mutate" },
            { action: "api_mutations_update_git_root_mutate" },
            { action: "api_resolvers_git_root_secrets_resolve" },
          ])
        }
      >
        <MockedProvider cache={getCache()} mocks={[mockedQueries]}>
          <ManagementModal
            finishTour={finishTour}
            groupName={""}
            initialValues={initialValues}
            isEditing={true}
            manyRows={false}
            modalMessages={{ message: "", type: "success" }}
            onClose={handleClose}
            onSubmitRepo={handleSubmit}
            runTour={false}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    // Repository fields
    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "url" })).toBeInTheDocument();
    });

    expect(screen.getByRole("textbox", { name: "url" })).toHaveValue(
      "https://gitlab.com/fluidattacks/universe"
    );

    await waitFor((): void => {
      expect(screen.queryAllByRole("link")).toHaveLength(3);
    });

    jest.clearAllMocks();
  });

  it("should render add envs modal for AWS cloudName", async (): Promise<void> => {
    expect.hasAssertions();

    const closeFunction: jest.Mock = jest.fn();
    render(
      <authzPermissionsContext.Provider
        value={
          new PureAbility([
            { action: "api_mutations_add_git_environment_secret_mutate" },
          ])
        }
      >
        <MockedProvider mocks={[mockedAddFileQuery]}>
          <AddEnvironment
            closeFunction={closeFunction}
            groupName={""}
            rootId={""}
          />
        </MockedProvider>
      </authzPermissionsContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByRole("textbox", { name: "url" })).toBeInTheDocument();
    });

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "urlType" }),
      ["CLOUD"]
    );

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "cloudName" }),
      ["AWS"]
    );

    // Present only for cloudName AWS and urlType CLOUD
    expect(screen.getByRole("textbox", { name: "url" })).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "accessKeyId" })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: "secretAccessKey" })
    ).toBeInTheDocument();

    await userEvent.selectOptions(
      screen.getByRole("combobox", { name: "cloudName" }),
      ["GCP"]
    );

    expect(
      screen.queryByRole("textbox", { name: "accessKeyId" })
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("textbox", { name: "secretAccessKey" })
    ).not.toBeInTheDocument();

    jest.clearAllMocks();
  });
});
