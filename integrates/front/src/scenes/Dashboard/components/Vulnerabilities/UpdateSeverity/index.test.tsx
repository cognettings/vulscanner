import type { MockedResponse } from "@apollo/client/testing";
import { MockedProvider } from "@apollo/client/testing";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { UpdateSeverity } from ".";
import {
  GET_VULN_SEVERITY_INFO,
  UPDATE_VULNERABILITIES_SEVERITY,
} from "scenes/Dashboard/components/Vulnerabilities/SeverityInfo/queries";
import type { IVulnDataTypeAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { msgSuccess } from "utils/notifications";

jest.mock("../../../../../utils/notifications", (): Record<string, unknown> => {
  const mockedNotifications: Record<string, () => Record<string, unknown>> =
    jest.requireActual("../../../../../utils/notifications");
  jest.spyOn(mockedNotifications, "msgSuccess").mockImplementation();

  return mockedNotifications;
});

describe("UpdateSeverity", (): void => {
  const vulnId = "af7a48b8-d8fc-41da-9282-d424fff563f0";
  const findingId = "438679960";
  const vulnerabilitiesData: IVulnDataTypeAttr[] = [
    {
      assigned: "",
      externalBugTrackingSystem: null,
      findingId,
      groupName: "testgroupname",
      historicTreatment: [
        {
          date: "",
          justification: "test justification",
          treatment: "UNTREATED",
          user: "",
        },
      ],
      id: vulnId,
      severity: "2",
      source: "asm",
      specific: "",
      state: "VULNERABLE",
      tag: "one",
      where: "",
    },
  ];
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
    expect(typeof UpdateSeverity).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    jest.clearAllMocks();
    jest.spyOn(console, "error").mockImplementation();
    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider addTypename={true} mocks={[mockVulnSeverityInfo]}>
          <UpdateSeverity
            findingId={findingId}
            handleCloseModal={jest.fn()}
            refetchData={jest.fn()}
            vulnerabilities={vulnerabilitiesData}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "severityVector" })
      ).toBeInTheDocument();
    });

    expect(
      screen.getByText(
        "searchFindings.tabDescription.updateVulnerabilitiesSeverityLabel"
      )
    ).toBeInTheDocument();

    const confirmButton = screen.getByRole("button", {
      name: "components.modal.confirm",
    });

    expect(confirmButton).toBeInTheDocument();
    expect(confirmButton).toBeEnabled();

    const cancelButton = screen.getByRole("button", {
      name: "group.findings.report.modalClose",
    });

    expect(cancelButton).toBeInTheDocument();
    expect(cancelButton).toBeEnabled();
  });

  it("should update vulnerabilities severity vector", async (): Promise<void> => {
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

    render(
      <MemoryRouter initialEntries={["/orgs/okada"]}>
        <MockedProvider
          addTypename={false}
          mocks={[mockVulnSeverityInfo, mockedMutation]}
        >
          <UpdateSeverity
            findingId={findingId}
            handleCloseModal={jest.fn()}
            refetchData={jest.fn()}
            vulnerabilities={vulnerabilitiesData}
          />
        </MockedProvider>
      </MemoryRouter>
    );

    await waitFor((): void => {
      expect(
        screen.queryByRole("textbox", { name: "severityVector" })
      ).toBeInTheDocument();
    });

    await userEvent.clear(screen.getByRole("textbox"));
    await userEvent.type(screen.getByRole("textbox"), modifiedCvssVector);

    await userEvent.click(
      screen.getByRole("button", {
        name: "components.modal.confirm",
      })
    );

    await waitFor((): void => {
      expect(msgSuccess).toHaveBeenCalledWith(
        "searchFindings.tabVuln.severityInfo.alerts.updatedSeverity",
        "groupAlerts.updatedTitle"
      );
    });
  });
});
