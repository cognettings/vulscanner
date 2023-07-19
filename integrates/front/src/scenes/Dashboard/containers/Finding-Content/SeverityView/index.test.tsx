import { MockedProvider } from "@apollo/client/testing";
import type { MockedResponse } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { GraphQLError } from "graphql";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { authzPermissionsContext } from "context/authz/config";
import { SeverityView } from "scenes/Dashboard/containers/Finding-Content/SeverityView";
import { GET_SEVERITY } from "scenes/Dashboard/containers/Finding-Content/SeverityView/queries";
import { msgError } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgError").mockImplementation();

  return mockedNotifications;
});

describe("SeverityView", (): void => {
  const mocks: readonly MockedResponse[] = [
    {
      request: {
        query: GET_SEVERITY,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        data: {
          finding: {
            cvssVersion: "3.1",
            id: "468603225",
            severity: {
              attackComplexity: 0.77,
              attackVector: 0.85,
              availabilityImpact: 0.56,
              availabilityRequirement: 1.5,
              confidentialityImpact: 0.56,
              confidentialityRequirement: 1.5,
              exploitability: 1,
              integrityImpact: 0.56,
              integrityRequirement: 1.5,
              modifiedAttackComplexity: 0.44,
              modifiedAttackVector: 0.62,
              modifiedAvailabilityImpact: 0,
              modifiedConfidentialityImpact: 0.22,
              modifiedIntegrityImpact: 0.22,
              modifiedPrivilegesRequired: 0.85,
              modifiedSeverityScope: 0,
              modifiedUserInteraction: 0.85,
              privilegesRequired: 0.85,
              remediationLevel: 1,
              reportConfidence: 1,
              severityScope: 1,
              userInteraction: 0.85,
            },
            severityVector:
              "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
          },
        },
      },
    },
  ];

  const mockError: readonly MockedResponse[] = [
    {
      request: {
        query: GET_SEVERITY,
        variables: {
          identifier: "438679960",
        },
      },
      result: {
        errors: [new GraphQLError("Access denied")],
      },
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SeverityView).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.spyOn(console, "error").mockImplementation();
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_severity_mutate" },
    ]);
    const { container } = render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={SeverityView}
              path={"/:groupName/vulns/:findingId/severity"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabSeverity.editable.label")
      ).toBeInTheDocument();
    });
    const numberOfTilesAndButtonTooltip: number = 12;

    expect(
      container.querySelectorAll(".__react_component_tooltip")
    ).toHaveLength(numberOfTilesAndButtonTooltip);
    expect(
      screen.queryByText("searchFindings.tabSeverity.reportConfidence.label")
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "searchFindings.tabSeverity.exploitability.options.proofOfConcept.label"
      )
    ).not.toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabSeverity.editable.label")
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.tabSeverity.editable.label")
    );
    await waitFor((): void => {
      screen.queryByText(
        "searchFindings.tabSeverity.exploitability.options.proofOfConcept.label"
      );
    });

    expect(
      container.querySelectorAll(".__react_component_tooltip")
    ).toHaveLength(1);
  });

  it("should render an error in component", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={SeverityView}
            path={"/:groupName/vulns/:findingId/severity"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(msgError).toHaveBeenCalledWith("groupAlerts.errorTextsad");
    });

    jest.clearAllMocks();
  });

  it("should render as editable", async (): Promise<void> => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_severity_mutate" },
    ]);
    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mocks}>
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <Route
              component={SeverityView}
              path={"/:groupName/vulns/:findingId/severity"}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabSeverity.editable.label")
      ).toBeInTheDocument();
    });
    await userEvent.click(
      screen.getByText("searchFindings.tabSeverity.editable.label")
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabSeverity.update")
      ).toBeInTheDocument();
    });
  });

  it("should render as readonly", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/TEST/vulns/438679960/severity"]}>
        <MockedProvider addTypename={false} mocks={mockError}>
          <Route
            component={SeverityView}
            path={"/:groupName/vulns/:findingId/severity"}
          />
        </MockedProvider>
      </MemoryRouter>
    );
    await waitFor((): void => {
      expect(
        screen.queryByText("searchFindings.tabSeverity.editable.label")
      ).not.toBeInTheDocument();
    });
  });
});
