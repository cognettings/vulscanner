import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import { TagContent } from "scenes/Dashboard/containers/TagContent";

describe("TagContent", (): void => {
  const mocks: MockedResponse = {
    request: {
      query: GET_ORGANIZATION_ID,
      variables: {
        organizationName: "testorg",
      },
    },
    result: {
      data: {
        organizationId: {
          id: "ORG#eb50af04-4d50-4e40-bab1-a3fe9f672f9d",
          name: "testorg",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof TagContent).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter
        initialEntries={["/orgs/testorg/portfolios/test-projects/analytics"]}
      >
        <MockedProvider addTypename={false} mocks={[mocks]}>
          <Route
            component={TagContent}
            path={"/orgs/:organizationName/portfolios/:tagName/analytics"}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(screen.getAllByRole("listitem")).toHaveLength(2);
    });

    expect(
      screen.getByText("organization.tabs.portfolios.tabs.indicators.text")
    ).toBeInTheDocument();

    jest.clearAllMocks();
  });
});
