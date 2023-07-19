import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { BrowserRouter, MemoryRouter } from "react-router-dom";

import type { IAcceptLegal, IUserRemember } from "./legal-notice/queries";
import {
  ACCEPT_LEGAL_MUTATION,
  GET_USER_REMEMBER,
} from "./legal-notice/queries";
import type { IUserOrganizations } from "./navbar/breadcrumb/queries";
import { GET_USER_ORGANIZATIONS } from "./navbar/breadcrumb/queries";

import { Dashboard } from ".";
import { getCache } from "utils/apollo";

const basicOrganizationsMock: MockedResponse<IUserOrganizations> = {
  request: {
    query: GET_USER_ORGANIZATIONS,
  },
  result: {
    data: {
      me: {
        __typename: "Me",
        organizations: [
          { __typename: "Organization", name: "test" },
          { __typename: "Organization", name: "test2" },
        ],
        userEmail: "test@test.com",
      },
    },
  },
};
const basicRememberMock: MockedResponse<IUserRemember> = {
  request: {
    query: GET_USER_REMEMBER,
  },
  result: {
    data: {
      me: {
        __typename: "Me",
        remember: true,
        userEmail: "test@test.com",
      },
    },
  },
};

describe("Dashboard", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Dashboard).toBe("function");
  });

  it("should apply start url", async (): Promise<void> => {
    expect.hasAssertions();

    jest.spyOn(console, "error").mockImplementation();
    jest.spyOn(console, "warn").mockImplementation();
    localStorage.setItem("start_url", "/orgs/test/groups/test");

    render(
      <BrowserRouter>
        <MockedProvider
          cache={getCache()}
          mocks={[basicOrganizationsMock, basicRememberMock]}
        >
          <Dashboard />
        </MockedProvider>
      </BrowserRouter>
    );

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
    expect(window.location.pathname).toBe("/orgs/test/groups/test");
    expect(localStorage.getItem("start_url")).toBeNull();

    window.history.pushState({}, "", "/");
  });

  it("should determine initial organization from user", async (): Promise<void> => {
    expect.hasAssertions();

    jest.spyOn(console, "error").mockImplementation();
    jest.spyOn(console, "warn").mockImplementation();

    render(
      <BrowserRouter>
        <MockedProvider
          cache={getCache()}
          mocks={[basicOrganizationsMock, basicRememberMock]}
        >
          <Dashboard />
        </MockedProvider>
      </BrowserRouter>
    );

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
    expect(window.location.pathname).toBe("/orgs/test");

    window.history.pushState({}, "", "/");
  });

  it("should determine initial organization from storage", async (): Promise<void> => {
    expect.hasAssertions();

    jest.spyOn(console, "error").mockImplementation();
    jest.spyOn(console, "warn").mockImplementation();
    localStorage.setItem("organization", JSON.stringify({ name: "stored" }));

    render(
      <BrowserRouter>
        <MockedProvider
          cache={getCache()}
          mocks={[basicOrganizationsMock, basicRememberMock]}
        >
          <Dashboard />
        </MockedProvider>
      </BrowserRouter>
    );

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
    expect(window.location.pathname).toBe("/orgs/stored");

    window.history.pushState({}, "", "/");
  });

  it("should open legal notice", async (): Promise<void> => {
    expect.hasAssertions();

    const userRememberMock: MockedResponse<IUserRemember> = {
      request: {
        query: GET_USER_REMEMBER,
      },
      result: {
        data: {
          me: {
            __typename: "Me",
            remember: false,
            userEmail: "test@test.com",
          },
        },
      },
    };
    const acceptLegalMock: MockedResponse<IAcceptLegal> = {
      request: {
        query: ACCEPT_LEGAL_MUTATION,
        variables: { remember: false },
      },
      result: {
        data: {
          acceptLegal: { success: true },
        },
      },
    };

    jest.spyOn(console, "error").mockImplementation();
    jest.spyOn(console, "warn").mockImplementation();
    jest
      .spyOn(document, "referrer", "get")
      .mockReturnValue("https://accounts.google.com/");

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider
          cache={getCache()}
          mocks={[basicOrganizationsMock, userRememberMock, acceptLegalMock]}
        >
          <Dashboard />
        </MockedProvider>
      </MemoryRouter>
    );

    expect(screen.queryByRole("main")).not.toBeInTheDocument();
    await expect(
      screen.findByText("legalNotice.title")
    ).resolves.toBeInTheDocument();

    const acceptButton = await screen.findByText("legalNotice.accept");
    await userEvent.click(acceptButton);

    await expect(screen.findByRole("main")).resolves.toBeInTheDocument();
    expect(screen.queryByRole("legalNotice.title")).not.toBeInTheDocument();
  });
});
