import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { APITokenForcesModal } from "scenes/Dashboard/components/APITokenForcesModal";
import {
  GET_FORCES_TOKEN,
  UPDATE_FORCES_TOKEN_MUTATION,
} from "scenes/Dashboard/components/APITokenForcesModal/queries";
import { msgError, msgSuccess } from "utils/notifications";

jest.mock("../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("Update access token modal", (): void => {
  const handleOnClose: jest.Mock = jest.fn();

  const revealButtonText: string = "updateForcesToken.revealToken";
  const generateButtonText: string = "updateForcesToken.generate";
  const resetButtonText: string = "updateForcesToken.reset";
  const copyButtonText: string = "updateForcesToken.copy.copy";
  const closeButtonText: string = "components.modal.cancel";

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof APITokenForcesModal).toBe("function");
  });

  it("should render a token modal with token and reset", async (): Promise<void> => {
    expect.hasAssertions();

    const beforeValue: string = "before value";
    const afterValue: string = "after value";
    const mockQueryFull: MockedResponse[] = [
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesExpDate: beforeValue,
              forcesToken: beforeValue,
              name: "unittesting",
            },
          },
        },
      },
      {
        request: {
          query: UPDATE_FORCES_TOKEN_MUTATION,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            updateForcesAccessToken: {
              sessionJwt: afterValue,
              success: true,
            },
          },
        },
      },
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesExpDate: afterValue,
              forcesToken: afterValue,
              name: "unittesting",
            },
          },
        },
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={mockQueryFull}>
        <APITokenForcesModal
          groupName={"unittesting"}
          onClose={handleOnClose}
          open={true}
        />
      </MockedProvider>
    );

    expect(screen.getByText(generateButtonText)).toBeDisabled();

    await userEvent.click(screen.getByText(revealButtonText));
    await waitFor((): void => {
      expect(screen.getByText(beforeValue)).toBeInTheDocument();
    });

    expect(screen.getByText(revealButtonText)).toBeDisabled();
    expect(screen.getByText(resetButtonText)).not.toHaveAttribute("disabled");

    await userEvent.click(screen.getByText(resetButtonText));
    await waitFor((): void => {
      expect(screen.queryByText(afterValue)).toBeInTheDocument();
    });

    expect(msgSuccess).toHaveBeenCalledWith(
      "updateForcesToken.successfully",
      "updateForcesToken.success"
    );

    await userEvent.click(screen.getByText(copyButtonText));

    expect(msgError).toHaveBeenCalledWith("updateForcesToken.copy.failed");

    jest.clearAllMocks();
  });

  it("should render a token modal with token and copy it", async (): Promise<void> => {
    expect.hasAssertions();

    const user = userEvent.setup();
    const expDate: string = "some date";
    const tokenValue: string = "some value";
    const mockQueryFull: MockedResponse[] = [
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unnittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesExpDate: expDate,
              forcesToken: tokenValue,
              name: "unnittesting",
            },
          },
        },
      },
    ];
    render(
      <MockedProvider addTypename={false} mocks={mockQueryFull}>
        <APITokenForcesModal
          groupName={"unnittesting"}
          onClose={handleOnClose}
          open={true}
        />
      </MockedProvider>
    );

    expect(screen.getByText(revealButtonText)).not.toBeDisabled();
    expect(screen.getByText(copyButtonText)).toBeDisabled();

    await userEvent.click(screen.getByText(revealButtonText));
    await waitFor((): void => {
      expect(screen.getByText(revealButtonText)).toBeDisabled();
    });
    await waitFor((): void => {
      expect(screen.getByText(copyButtonText)).not.toBeDisabled();
    });

    expect(screen.getByText(resetButtonText)).not.toBeDisabled();
    expect(screen.getByText(tokenValue)).toBeInTheDocument();

    await user.click(screen.getByText(copyButtonText));

    expect(msgSuccess).toHaveBeenCalledWith(
      "updateForcesToken.copy.successfully",
      "updateForcesToken.copy.success"
    );

    jest.clearAllMocks();
  });

  it("should render a token modal without token", async (): Promise<void> => {
    expect.hasAssertions();

    const mockQueryNull: MockedResponse[] = [
      {
        request: {
          query: GET_FORCES_TOKEN,
          variables: {
            groupName: "unnittesting",
          },
        },
        result: {
          data: {
            group: {
              forcesExpDate: null,
              forcesToken: null,
              name: "unnittesting",
            },
          },
        },
      },
    ];

    render(
      <MockedProvider addTypename={false} mocks={mockQueryNull}>
        <APITokenForcesModal
          groupName={"unnittesting"}
          onClose={handleOnClose}
          open={true}
        />
      </MockedProvider>
    );

    const title: string = "updateForcesToken.title";

    expect(screen.getByText(title)).toBeInTheDocument();

    // When the token is revealed and does not exist, it cannot be copied
    await userEvent.click(screen.getByText(revealButtonText));
    await waitFor((): void => {
      expect(screen.getByText(generateButtonText)).not.toBeDisabled();
    });

    expect(screen.getByText(copyButtonText)).toBeDisabled();

    expect(screen.getByText(revealButtonText)).toBeDisabled();

    await userEvent.click(screen.getByText(closeButtonText));

    expect(handleOnClose).toHaveBeenCalledTimes(1);

    jest.clearAllMocks();
  });
});
