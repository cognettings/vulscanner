import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import dayjs from "dayjs";
import React from "react";

import { AccessTokenModal } from "pages/home/dashboard/navbar/user-profile/api-token-modal";
import {
  ADD_ACCESS_TOKEN,
  GET_ACCESS_TOKEN,
  INVALIDATE_ACCESS_TOKEN_MUTATION,
} from "pages/home/dashboard/navbar/user-profile/api-token-modal/queries";
import type { IAddAccessTokenAttr } from "pages/home/dashboard/navbar/user-profile/api-token-modal/types";
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

describe("Update access token modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  const msToSec: number = 1000;
  const yyyymmdd: number = 10;

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AccessTokenModal).toBe("function");
  });

  it("should render an add access token modal", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryFalse: MockedResponse[] = [
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessTokens: [],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider cache={getCache()} mocks={mockQueryFalse}>
        <AccessTokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    expect(screen.getByText("updateAccessToken.title")).toBeInTheDocument();

    await waitFor((): void => {
      expect(
        screen.queryByText("updateAccessToken.buttons.add")
      ).toBeInTheDocument();
    });

    expect(screen.getByText("table.noDataIndication")).toBeInTheDocument();

    await userEvent.click(screen.getByText("updateAccessToken.buttons.add"));

    await waitFor((): void => {
      expect(
        screen.queryByText("updateAccessToken.addTitle")
      ).toBeInTheDocument();
    });

    expect(screen.getByText("components.modal.confirm")).not.toBeDisabled();
    expect(
      screen.getByText("updateAccessToken.expirationTime")
    ).toBeInTheDocument();
    expect(
      screen.getByText("updateAccessToken.fields.name")
    ).toBeInTheDocument();

    await userEvent.click(screen.getByText("components.modal.cancel"));

    await userEvent.click(screen.getAllByRole("button")[0]);

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });

  it("should render a token creation date", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryTrue: MockedResponse[] = [
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessTokens: [
                {
                  __typename: "AccessToken",
                  id: "a8e91ab7-29c8-4f74-b8d4-3c7d69cf187f",
                  issuedAt: 1687376518,
                  lastUse: dayjs.utc().toISOString(),
                  name: "FirstToken",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: INVALIDATE_ACCESS_TOKEN_MUTATION,
          variables: {
            id: "a8e91ab7-29c8-4f74-b8d4-3c7d69cf187f",
          },
        },
        result: {
          data: {
            invalidateAccessToken: {
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessTokens: [],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider cache={getCache()} mocks={mockQueryTrue}>
        <AccessTokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.queryByText("FirstToken")).toBeInTheDocument();
    });

    expect(screen.getAllByRole("row")).toHaveLength(2);
    expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
      [
        "FirstToken",
        "2023-06-21",
        "a few seconds ago",
        "updateAccessToken.buttons.revoke",
      ].join("")
    );

    await userEvent.click(screen.getByText("updateAccessToken.buttons.revoke"));

    expect(
      screen.getByText("updateAccessToken.invalidate")
    ).toBeInTheDocument();

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "updateAccessToken.delete",
        "updateAccessToken.invalidated"
      );
    });
    await waitFor((): void => {
      expect(screen.getAllByRole("row")[1].textContent).toBe(
        "table.noDataIndication"
      );
    });

    await userEvent.click(screen.queryAllByRole("button")[0]);

    await waitFor((): void => {
      expect(handleOnClose).toHaveBeenCalledTimes(1);
    });

    jest.clearAllMocks();
  });

  it("should render a new access token", async (): Promise<void> => {
    expect.hasAssertions();

    const expirationTime: string = dayjs()
      .add(1, "month")
      .toISOString()
      .substring(0, yyyymmdd);
    const addAccessToken: IAddAccessTokenAttr = {
      addAccessToken: {
        sessionJwt: "dummyJwt",
        success: true,
      },
    };
    const mockMutation: MockedResponse[] = [
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessTokens: [],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
      {
        request: {
          query: ADD_ACCESS_TOKEN,
          variables: {
            expirationTime: Math.floor(
              new Date(expirationTime).getTime() / msToSec
            ),
            name: "AnotherToken",
          },
        },
        result: {
          data: {
            ...addAccessToken,
          },
        },
      },
      {
        request: {
          query: GET_ACCESS_TOKEN,
        },
        result: {
          data: {
            me: {
              accessTokens: [
                {
                  __typename: "AccessToken",
                  id: "28565d7d-0eb8-48a3-85f3-4fd6d03e3725",
                  issuedAt: 1687376518,
                  lastUse: null,
                  name: "AnotherToken",
                },
              ],
              userEmail: "test@fluidattacks.com",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider cache={getCache()} mocks={mockMutation}>
        <AccessTokenModal onClose={handleOnClose} open={true} />
      </MockedProvider>
    );

    expect(screen.getByText("updateAccessToken.title")).toBeInTheDocument();

    await waitFor((): void => {
      expect(
        screen.queryByText("updateAccessToken.buttons.add")
      ).toBeInTheDocument();
    });

    expect(screen.getByText("table.noDataIndication")).toBeInTheDocument();

    await userEvent.click(screen.getByText("updateAccessToken.buttons.add"));

    await waitFor((): void => {
      expect(
        screen.queryByText("updateAccessToken.addTitle")
      ).toBeInTheDocument();
    });

    await userEvent.type(
      screen.getByLabelText("expirationTime"),
      expirationTime
    );
    await userEvent.type(
      screen.getByRole("textbox", { name: "name" }),
      "AnotherToken"
    );

    await userEvent.click(screen.getByText("components.modal.confirm"));

    await waitFor((): void => {
      expect(screen.getByText("updateAccessToken.message")).toBeInTheDocument();
    });

    await waitFor((): void => {
      expect(screen.getAllByRole("row")[1].textContent).toStrictEqual(
        [
          "AnotherToken",
          "2023-06-21",
          "Never",
          "updateAccessToken.buttons.revoke",
        ].join("")
      );
    });

    expect(msgSuccess).toHaveBeenCalledWith(
      "updateAccessToken.successfully",
      "updateAccessToken.success"
    );

    await userEvent.click(screen.getByText("updateAccessToken.copy.copy"));

    expect(msgError).toHaveBeenCalledWith("updateAccessToken.copy.failed");

    jest.clearAllMocks();
  });
});
