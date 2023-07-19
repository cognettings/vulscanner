import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { act } from "react-dom/test-utils";

import { AddOrganizationModal } from "pages/home/dashboard/navbar/breadcrumb/add-organization-modal";
import { ADD_NEW_ORGANIZATION } from "pages/home/dashboard/navbar/breadcrumb/add-organization-modal/queries";
import { getCache } from "utils/apollo";
import { COUNTRIES_URL } from "utils/countries";

const handleCloseModal: jest.Mock = jest.fn();
const mockHistoryPush: jest.Mock = jest.fn();
jest.mock("react-router-dom", (): Record<string, unknown> => {
  const mockedRouter: Record<string, () => Record<string, unknown>> =
    jest.requireActual("react-router-dom");

  return {
    ...mockedRouter,
    useHistory: (): Record<string, unknown> => ({
      ...mockedRouter.useHistory(),
      push: mockHistoryPush,
    }),
  };
});

describe("Add organization modal", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof AddOrganizationModal).toBe("function");
  });

  it("should render component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mocks: MockedResponse[] = [];

    render(
      <MockedProvider cache={getCache()} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    expect(screen.getByRole("textbox")).toBeInTheDocument();

    await userEvent.click(screen.getByText("components.modal.cancel"));

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });
  });

  it("should create an organization", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    const mockedFetch: FetchMockStatic = fetch as FetchMockStatic &
      typeof fetch;
    mockedFetch.mock(COUNTRIES_URL, {
      body: [{ id: "CO", name: "Colombia" }],
      status: 200,
    });

    const mocks: MockedResponse[] = [
      {
        request: {
          query: ADD_NEW_ORGANIZATION,
          variables: {
            country: "Colombia",
            name: "ESDEATH",
          },
        },
        result: {
          data: {
            addOrganization: {
              organization: {
                id: "ORG#eb50af04-4d50-4e40-bab1-a3fe9f672f9d",
                name: "esdeath",
              },
              success: true,
            },
          },
        },
      },
    ];
    render(
      <MockedProvider cache={getCache()} mocks={mocks}>
        <AddOrganizationModal onClose={handleCloseModal} open={true} />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(screen.getByLabelText("country").children.length).toBeGreaterThan(
        1
      );
    });

    await act(async (): Promise<void> => {
      await userEvent.type(screen.getByLabelText("name"), "esdeath");
      await userEvent.selectOptions(screen.getByLabelText("country"), [
        "Colombia",
      ]);

      await userEvent.click(screen.getByText("components.modal.confirm"));
    });

    await waitFor((): void => {
      expect(handleCloseModal).toHaveBeenCalledTimes(1);
    });

    await waitFor((): void => {
      expect(mockHistoryPush).toHaveBeenCalledWith("/orgs/esdeath/");
    });
  });
});
