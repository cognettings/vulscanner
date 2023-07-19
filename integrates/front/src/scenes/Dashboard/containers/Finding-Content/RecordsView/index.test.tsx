import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { authzPermissionsContext } from "context/authz/config";
import { RecordsView } from "scenes/Dashboard/containers/Finding-Content/RecordsView";
import { GET_FINDING_RECORDS } from "scenes/Dashboard/containers/Finding-Content/RecordsView/queries";

describe("FindingRecordsView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_FINDING_RECORDS,
        variables: { findingId: "422286126" },
      },
      result: {
        data: {
          finding: {
            id: "422286126",
            records: JSON.stringify([
              {
                Character: "Cobra Commander",
                Genre: "action",
                Release: "2013",
                Title: "G.I. Joe: Retaliation",
              },
              {
                Character: "Tony Stark",
                Genre: "action",
                Release: "2008",
                Title: "Iron Man",
              },
            ]),
          },
        },
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof RecordsView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/422286126/records"]}
      >
        <MockedProvider mocks={mocks}>
          <Route
            component={RecordsView}
            path={
              "/orgs/:organizationName/groups/:groupName/vulns/:findingId/records"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("columnheader")).toHaveLength(4);
    });
  });

  it("should render as editable", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_evidence_mutate" },
    ]);
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/422286126/records"]}
      >
        <MockedProvider mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={RecordsView}
              path={
                "/orgs/:organizationName/groups/:groupName/vulns/:findingId/records"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabRecords.editable")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("searchFindings.tabRecords.editable")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.update")
      ).toBeInTheDocument();
    });
  });

  it("should render as readonly", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/422286126/records"]}
      >
        <MockedProvider mocks={mocks}>
          <Route
            component={RecordsView}
            path={
              "/orgs/:organizationName/groups/:groupName/vulns/:findingId/records"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(screen.queryAllByRole("row")).toHaveLength(3);
    });

    expect(
      screen.queryByText("searchFindings.tabRecords.editable")
    ).not.toBeInTheDocument();
  });

  it("should render delete button", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_evidence_mutate" },
    ]);
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/422286126/records"]}
      >
        <MockedProvider mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={RecordsView}
              path={
                "/orgs/:organizationName/groups/:groupName/vulns/:findingId/records"
              }
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabRecords.editable")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("searchFindings.tabRecords.editable")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabEvidence.remove")
      ).toBeInTheDocument();
    });
  });

  it("should render empty UI", async (): Promise<void> => {
    expect.hasAssertions();

    const emptyMocks: readonly MockedResponse[] = [
      {
        request: {
          query: GET_FINDING_RECORDS,
          variables: { findingId: "422286126" },
        },
        result: {
          data: {
            finding: {
              id: "422286126",
              records: "[]",
            },
          },
        },
      },
    ];
    render(
      <MemoryRouter
        initialEntries={["/orgs/okada/groups/TEST/vulns/422286126/records"]}
      >
        <MockedProvider mocks={emptyMocks}>
          <Route
            component={RecordsView}
            path={
              "/orgs/:organizationName/groups/:groupName/vulns/:findingId/records"
            }
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("group.findings.records.noData")
      ).toBeInTheDocument();
    });
  });
});
