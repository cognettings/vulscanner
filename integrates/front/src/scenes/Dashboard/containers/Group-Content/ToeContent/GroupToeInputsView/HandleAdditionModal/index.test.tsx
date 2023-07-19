import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { ADD_TOE_INPUT, GET_ROOTS } from "./queries";

import { HandleAdditionModal } from ".";
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

describe("Handle addition modal", (): void => {
  const refetchDataFn: jest.Mock = jest.fn();
  const handleCloseModal: jest.Mock = jest.fn();
  const mocksMutation: MockedResponse = {
    request: {
      query: ADD_TOE_INPUT,
      variables: {
        component: "https://app.fluidattacks.com/test/test",
        entryPoint: "test",
        groupName: "groupname",
        rootId: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
      },
    },
    result: { data: { addToeInput: { success: true } } },
  };
  const queryMock: MockedResponse = {
    request: {
      query: GET_ROOTS,
      variables: { groupName: "groupname" },
    },
    result: {
      data: {
        group: {
          __typename: "Group",
          name: "test",
          roots: [
            {
              __typename: "GitRoot",
              gitEnvironmentUrls: [
                {
                  __typename: "GitEnvironmentUrl",
                  id: "00fbe3579a253b43239954a545dc0536e6c83094",
                  url: "https://app.fluidattacks.com/test",
                  urlType: "URL",
                },
              ],
              id: "4039d098-ffc5-4984-8ed3-eb17bca98e19",
              nickname: "universe",
              state: "ACTIVE",
            },
          ],
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HandleAdditionModal).toBe("function");
  });

  it("should render modal", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MockedProvider cache={getCache()} mocks={[queryMock]}>
        <HandleAdditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={refetchDataFn}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(
        screen.getByText("group.toe.inputs.addModal.title")
      ).toBeInTheDocument();
    });

    expect(
      screen.queryByRole("combobox", { name: "environmentUrl" })
    ).toHaveValue("https://app.fluidattacks.com/test");
    expect(screen.getByText("Root")).toBeInTheDocument();
    expect(screen.getByText("Environment")).toBeInTheDocument();
    expect(
      screen.getByText("group.toe.inputs.addModal.fields.component")
    ).toBeInTheDocument();
    expect(
      screen.getByText("group.toe.inputs.addModal.fields.entryPoint")
    ).toBeInTheDocument();
  });

  it("should submit form", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <MockedProvider cache={getCache()} mocks={[mocksMutation, queryMock]}>
        <HandleAdditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={refetchDataFn}
        />
      </MockedProvider>
    );

    await screen.findByText("group.toe.inputs.addModal.title");
    await waitFor((): void => {
      expect(
        screen.getByRole("combobox", { name: "rootNickname" })
      ).toHaveValue("universe");
    });
    await waitFor((): void => {
      expect(
        screen.getByRole("combobox", {
          name: "environmentUrl",
        })
      ).toHaveValue("https://app.fluidattacks.com/test");
    });

    expect(
      screen.queryByRole("combobox", {
        name: "environmentUrl",
      })
    ).toBeInTheDocument();

    const rootInput = screen.getByRole("combobox", { name: "rootNickname" });
    const environmentInput = screen.getByRole("combobox", {
      name: "environmentUrl",
    });
    const componentInput = screen.getByRole("textbox", { name: "path" });
    const entryPointInput = screen.getByRole("textbox", { name: "entryPoint" });

    fireEvent.change(componentInput, { target: { value: "test" } });
    fireEvent.change(entryPointInput, { target: { value: "test" } });

    expect(rootInput).toHaveValue("universe");
    expect(environmentInput).toHaveValue("https://app.fluidattacks.com/test");
    expect(componentInput).toHaveValue("test");
    expect(entryPointInput).toHaveValue("test");

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.inputs.addModal.alerts.success",
        "groupAlerts.titleSuccess"
      );
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(refetchDataFn).toHaveBeenCalledTimes(1);
  });

  it("should submit form non gitroot", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mocksNonGitRootMutation: MockedResponse = {
      request: {
        query: ADD_TOE_INPUT,
        variables: {
          component: "https://app.test.test:443/test",
          entryPoint: "test",
          groupName: "groupname",
          rootId: "8493c82f-2860-4902-86fa-75b0fef76034",
        },
      },
      result: { data: { addToeInput: { success: true } } },
    };
    const queryNonGitRootMock: MockedResponse = {
      request: {
        query: GET_ROOTS,
        variables: { groupName: "groupname" },
      },
      result: {
        data: {
          group: {
            __typename: "Group",
            name: "test",
            roots: [
              {
                __typename: "URLRoot",
                host: "app.test.test",
                id: "8493c82f-2860-4902-86fa-75b0fef76034",
                nickname: "url_root_1",
                path: "/",
                port: 443,
                protocol: "HTTPS",
                query: null,
                state: "ACTIVE",
              },
              {
                __typename: "IPRoot",
                id: "d312f0b9-da49-4d2b-a881-bed438875e99",
                nickname: "ip_root_1",
              },
            ],
          },
        },
      },
    };

    render(
      <MockedProvider
        cache={getCache()}
        mocks={[mocksNonGitRootMutation, queryNonGitRootMock]}
      >
        <HandleAdditionModal
          groupName={"groupname"}
          handleCloseModal={handleCloseModal}
          refetchData={refetchDataFn}
        />
      </MockedProvider>
    );

    await screen.findByText("group.toe.inputs.addModal.title");
    await waitFor((): void => {
      expect(
        screen.getByRole("combobox", { name: "rootNickname" })
      ).toHaveValue("url_root_1");
    });

    expect(
      screen.queryByRole("combobox", {
        name: "environmentUrl",
      })
    ).not.toBeInTheDocument();

    const rootInput = screen.getByRole("combobox", { name: "rootNickname" });
    const componentInput = screen.getByRole("textbox", { name: "path" });
    const entryPointInput = screen.getByRole("textbox", { name: "entryPoint" });

    fireEvent.change(componentInput, { target: { value: "test" } });
    fireEvent.change(entryPointInput, { target: { value: "test" } });

    expect(rootInput).toHaveValue("url_root_1");
    expect(componentInput).toHaveValue("test");
    expect(entryPointInput).toHaveValue("test");

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "group.toe.inputs.addModal.alerts.success",
        "groupAlerts.titleSuccess"
      );
    });

    expect(handleCloseModal).toHaveBeenCalledTimes(1);
    expect(refetchDataFn).toHaveBeenCalledTimes(1);
  });
});
