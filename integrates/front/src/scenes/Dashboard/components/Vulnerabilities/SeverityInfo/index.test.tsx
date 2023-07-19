import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import {
  GET_VULN_SEVERITY_INFO,
  UPDATE_VULNERABILITIES_SEVERITY,
} from "./queries";

import { SeverityInfo } from ".";
import { authzPermissionsContext } from "context/authz/config";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("VulnerabilitySeverityInfo", (): void => {
  const vulnId = "af7a48b8-d8fc-41da-9282-d424fff563f0";
  const findingId = "438679960";
  const mockVulnSeverityInfo: MockedResponse = {
    request: {
      query: GET_VULN_SEVERITY_INFO,
      variables: {
        vulnId,
      },
    },
    result: {
      data: {
        vulnerability: {
          __typename: "Vulnerability",
          id: vulnId,
          severityTemporalScore: 3.8,
          severityVector:
            "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        },
      },
    },
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SeverityInfo).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const { container } = render(
      <MemoryRouter
        initialEntries={[
          "/TEST/vulns/438679960/locations/af7a48b8-d8fc-41da-9282-d424fff563f0",
        ]}
      >
        <MockedProvider addTypename={true} mocks={[mockVulnSeverityInfo]}>
          <SeverityInfo
            findingId={findingId}
            refetchData={jest.fn()}
            vulnerabilityId={vulnId}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabVuln.severityInfo.severityVectorTitle"
        )
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText(
        "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C"
      )
    ).toBeInTheDocument();
    expect(screen.getByText("3.8")).toBeInTheDocument();
    expect(screen.getByText("Low")).toBeInTheDocument();

    const numberOfTilesAndButtonTooltip: number = 11;

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
  });

  it("should update vulnerability severity vector", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    jest.spyOn(console, "error").mockImplementation();
    jest.spyOn(console, "warn").mockImplementation();

    const modifiedCvssVector = "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H";
    const mockedMutation: MockedResponse = {
      request: {
        query: UPDATE_VULNERABILITIES_SEVERITY,
        variables: {
          cvssVector: modifiedCvssVector,
          findingId,
          vulnerabilityIds: [vulnId],
        },
      },
      result: {
        data: {
          updateVulnerabilitiesSeverity: {
            success: true,
          },
        },
      },
    };
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_vulnerabilities_severity_mutate" },
    ]);

    const { container } = render(
      <MemoryRouter
        initialEntries={[
          "/TEST/vulns/438679960/locations/af7a48b8-d8fc-41da-9282-d424fff563f0",
        ]}
      >
        <MockedProvider
          addTypename={false}
          mocks={[mockVulnSeverityInfo, mockedMutation]}
        >
          <authzPermissionsContext.Provider value={mockedPermissions}>
            <SeverityInfo
              findingId={findingId}
              refetchData={jest.fn()}
              vulnerabilityId={vulnId}
            />
          </authzPermissionsContext.Provider>
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.getByText(
          "searchFindings.tabVuln.severityInfo.severityVectorTitle"
        )
      ).toBeInTheDocument();
    });

    // The Edit button tooltip now is visible
    const numberOfTilesAndButtonTooltip: number = 12;

    expect(
      container.querySelectorAll(".__react_component_tooltip")
    ).toHaveLength(numberOfTilesAndButtonTooltip);

    const editButton = screen.getByRole("button", {
      name: "searchFindings.tabVuln.additionalInfo.buttons.edit.text",
    });

    expect(editButton).toBeInTheDocument();
    expect(editButton).toBeEnabled();

    await userEvent.click(editButton);

    await waitFor((): void => {
      expect(
        screen.getByRole("button", {
          name: "searchFindings.tabVuln.additionalInfo.buttons.save.text",
        })
      ).toBeInTheDocument();
    });

    // Severity score pill nor Severity Tiles are not visible on Edit Mode
    expect(screen.queryByText("3.8")).not.toBeInTheDocument();
    expect(screen.queryByText("Low")).not.toBeInTheDocument();

    const numberOfTilesAndButtonTooltipEditMode: number = 2;

    expect(
      container.querySelectorAll(".__react_component_tooltip")
    ).toHaveLength(numberOfTilesAndButtonTooltipEditMode);
    expect(
      screen.queryByText("searchFindings.tabSeverity.reportConfidence.label")
    ).not.toBeInTheDocument();

    const saveButton = screen.getByRole("button", {
      name: "searchFindings.tabVuln.additionalInfo.buttons.save.text",
    });

    expect(saveButton).toBeDisabled();

    await userEvent.clear(screen.getByRole("textbox"));
    await userEvent.type(screen.getByRole("textbox"), modifiedCvssVector);

    expect(saveButton).toBeEnabled();

    await userEvent.click(saveButton);

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.tabVuln.severityInfo.alerts.updatedSeverity",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
