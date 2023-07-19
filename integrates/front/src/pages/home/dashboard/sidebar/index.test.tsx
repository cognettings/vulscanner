import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { GET_ORG_GROUPS } from "./queries";

import { Sidebar } from ".";
import { featurePreviewContext } from "context/featurePreview";
import { getCache } from "utils/apollo";

describe("Sidebar", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_ORG_GROUPS,
        variables: {
          org: "okada",
        },
      },
      result: {
        data: {
          organizationId: {
            __typename: "Organization",
            groups: [
              {
                __typename: "Group",
                name: "group1",
              },
              {
                __typename: "Group",
                name: "group2",
              },
            ],
            name: "okada",
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Sidebar).toBe("function");
  });

  it("should render sidebar component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <featurePreviewContext.Provider value={{ featurePreview: false }}>
        <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
          <Sidebar />
        </MemoryRouter>
      </featurePreviewContext.Provider>
    );

    await waitFor((): void => {
      expect(screen.getByRole("link", { name: "App logo" })).toHaveAttribute(
        "href",
        "/home"
      );
    });
  });

  it("should render sidebar fp component", (): void => {
    expect.hasAssertions();

    jest.clearAllMocks();

    render(
      <featurePreviewContext.Provider value={{ featurePreview: true }}>
        <MemoryRouter initialEntries={["/orgs/okada/groups"]}>
          <MockedProvider cache={getCache()} mocks={mocks}>
            <Route path={"/orgs/:organizationName"}>
              <Sidebar />
            </Route>
          </MockedProvider>
        </MemoryRouter>
      </featurePreviewContext.Provider>
    );

    const appLogo = screen.getAllByRole("link");

    expect(appLogo[0]).toHaveAttribute("href", "/home");
    expect(appLogo[1]).toHaveAttribute("href", "/orgs/okada/groups");
    expect(appLogo[2]).toHaveAttribute("href", "/orgs/okada/analytics");
    expect(appLogo[3]).toHaveAttribute("href", "/orgs/okada/policies");
    expect(appLogo[4]).toHaveAttribute("href", "/orgs/okada/portfolios");
    expect(appLogo[5]).toHaveAttribute("href", "/orgs/okada/outside");
    expect(appLogo[6]).toHaveAttribute("href", "/orgs/okada/credentials");
    expect(appLogo[7]).toHaveAttribute("href", "/orgs/okada/compliance");
  });
});
