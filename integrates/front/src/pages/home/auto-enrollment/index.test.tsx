import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen } from "@testing-library/react";
import type { FetchMockStatic } from "fetch-mock";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { GET_STAKEHOLDER_GROUPS } from "./queries";
import type { IGetStakeholderGroupsResult } from "./types";
import { EMAIL_DOMAINS_URL } from "./utils";

import { Autoenrollment } from ".";
import { getCache } from "utils/apollo";
import { COUNTRIES_URL } from "utils/countries";

describe("Autoenrollment", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Autoenrollment).toBe("function");
  });

  it("should render corporate only", async (): Promise<void> => {
    expect.hasAssertions();

    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            trial: null,
            userEmail: "jdoe@personal.com",
            userName: "John Doe",
          },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { body: "personal.com", status: 200 });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(
      screen.findByText("autoenrollment.corporateOnly")
    ).resolves.toBeInTheDocument();

    mockedFetch.reset();
  });

  it("should render already in trial", async (): Promise<void> => {
    expect.hasAssertions();

    const groupsMock: MockedResponse<IGetStakeholderGroupsResult> = {
      request: {
        query: GET_STAKEHOLDER_GROUPS,
      },
      result: {
        data: {
          me: {
            organizations: [],
            trial: {
              completed: false,
              startDate: "2022-12-06T07:40:16.114232",
            },
            userEmail: "jdoe@fluidattacks.com",
            userName: "John Doe",
          },
        },
      },
    };

    const mockedFetch = fetch as FetchMockStatic & typeof fetch;
    mockedFetch.mock(EMAIL_DOMAINS_URL, { status: 200, text: "" });
    mockedFetch.mock(COUNTRIES_URL, { body: "[]", status: 200 });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <MockedProvider cache={getCache()} mocks={[groupsMock]}>
          <Autoenrollment />
        </MockedProvider>
      </MemoryRouter>
    );

    await expect(
      screen.findByText("autoenrollment.alreadyInTrial")
    ).resolves.toBeInTheDocument();

    mockedFetch.reset();
  });
});
