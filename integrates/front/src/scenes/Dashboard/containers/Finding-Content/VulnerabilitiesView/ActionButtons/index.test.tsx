import { PureAbility } from "@casl/ability";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { ActionButtons } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/ActionButtons";
import { msgInfo } from "utils/notifications";

jest.mock(
  "../../../../../../utils/notifications",
  (): Record<string, unknown> => {
    const mockedNotifications: Record<string, () => Record<string, unknown>> =
      jest.requireActual("../../../../../../utils/notifications");
    jest.spyOn(mockedNotifications, "msgInfo").mockImplementation();

    return mockedNotifications;
  }
);

describe("ActionButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toBe("function");
  });

  it("should render a component without permissions", (): void => {
    expect.hasAssertions();

    render(
      <authzPermissionsContext.Provider value={new PureAbility([])}>
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
        >
          <ActionButtons
            areRejectedVulns={false}
            areRequestedZeroRiskVulns={true}
            areSubmittedVulns={true}
            areVulnsPendingOfAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isRequestingReattack={false}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onNotify={jest.fn()}
            onRequestReattack={jest.fn()}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            status={"VULNERABLE"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("should render a component with only the edit button", (): void => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider
          value={new PureAbility([{ action: "can_report_vulnerabilities" }])}
        >
          <ActionButtons
            areRejectedVulns={false}
            areRequestedZeroRiskVulns={true}
            areSubmittedVulns={true}
            areVulnerableLocations={true}
            areVulnsPendingOfAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isRequestingReattack={false}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onNotify={jest.fn()}
            onRequestReattack={jest.fn()}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            status={"VULNERABLE"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.getByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();
  });

  it("should render request verification", async (): Promise<void> => {
    expect.hasAssertions();

    const onRequestReattack: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_request_vulnerabilities_verification_mutate" },
      { action: "api_mutations_update_vulnerabilities_severity_mutate" },
      { action: "api_mutations_update_vulnerabilities_treatment_mutate" },
    ]);
    const mockedServices = new PureAbility<string>([
      { action: "is_continuous" },
      { action: "can_report_vulnerabilities" },
    ]);
    const { rerender } = render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          <ActionButtons
            areRejectedVulns={false}
            areRequestedZeroRiskVulns={true}
            areSubmittedVulns={true}
            areVulnerableLocations={true}
            areVulnsPendingOfAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isRequestingReattack={false}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onNotify={jest.fn()}
            onRequestReattack={onRequestReattack}
            onUpdateSeverity={jest.fn()}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            status={"VULNERABLE"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(3);
    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabDescription.requestVerify.text")
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "searchFindings.tabDescription.updateVulnSeverityButton"
      )
    ).toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.requestVerify.text")
    );
    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          <ActionButtons
            areRejectedVulns={false}
            areRequestedZeroRiskVulns={true}
            areSubmittedVulns={true}
            areVulnerableLocations={true}
            areVulnsPendingOfAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isRequestingReattack={true}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onNotify={jest.fn()}
            onRequestReattack={onRequestReattack}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            status={"VULNERABLE"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );
    await waitFor((): void => {
      expect(onRequestReattack).toHaveBeenCalledTimes(1);
    });

    expect(msgInfo).toHaveBeenCalledWith(
      "searchFindings.tabVuln.info.text",
      "searchFindings.tabVuln.info.title",
      true
    );
    expect(
      screen.queryByText("searchFindings.tabDescription.cancelVerify")
    ).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabVuln.buttons.edit")
    ).not.toBeInTheDocument();

    await userEvent.click(
      screen.getByText("searchFindings.tabDescription.cancelVerify")
    );

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <authzGroupContext.Provider value={mockedServices}>
          <ActionButtons
            areRejectedVulns={false}
            areRequestedZeroRiskVulns={true}
            areSubmittedVulns={true}
            areVulnerableLocations={true}
            areVulnsPendingOfAcceptance={true}
            areVulnsSelected={false}
            isEditing={false}
            isFindingReleased={true}
            isOpen={false}
            isRequestingReattack={false}
            isVerified={false}
            isVerifying={false}
            onEdit={jest.fn()}
            onNotify={jest.fn()}
            onRequestReattack={onRequestReattack}
            onUpdateSeverity={jest.fn()}
            onVerify={jest.fn()}
            openHandleAcceptance={jest.fn()}
            openModal={jest.fn()}
            status={"VULNERABLE"}
          />
        </authzGroupContext.Provider>
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText("searchFindings.tabDescription.cancelVerify")
    ).not.toBeInTheDocument();
    expect(msgInfo).toHaveBeenCalledWith(
      "searchFindings.tabVuln.info.text",
      "searchFindings.tabVuln.info.title",
      false
    );
  });

  it("should render update severity", async (): Promise<void> => {
    expect.hasAssertions();

    const onUpdateSeverity: jest.Mock = jest.fn();
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_vulnerabilities_severity_mutate" },
    ]);
    const { rerender } = render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areRequestedZeroRiskVulns={false}
          areSubmittedVulns={false}
          areVulnsPendingOfAcceptance={false}
          areVulnsSelected={false}
          isEditing={false}
          isOpen={false}
          isRequestingReattack={false}
          isVerifying={false}
          onEdit={jest.fn()}
          onRequestReattack={jest.fn()}
          onUpdateSeverity={onUpdateSeverity}
          onVerify={jest.fn()}
          openHandleAcceptance={jest.fn()}
          openModal={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByRole("button")).toHaveLength(1);

    const updateSeverityButtonDisabled = screen.getByRole("button", {
      name: "searchFindings.tabDescription.updateVulnSeverityButton",
    });

    expect(updateSeverityButtonDisabled).toBeInTheDocument();
    expect(updateSeverityButtonDisabled).toBeDisabled();

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          areRequestedZeroRiskVulns={false}
          areSubmittedVulns={false}
          areVulnsPendingOfAcceptance={false}
          areVulnsSelected={true}
          isEditing={false}
          isOpen={false}
          isRequestingReattack={false}
          isVerifying={false}
          onEdit={jest.fn()}
          onRequestReattack={jest.fn()}
          onUpdateSeverity={onUpdateSeverity}
          onVerify={jest.fn()}
          openHandleAcceptance={jest.fn()}
          openModal={jest.fn()}
        />
      </authzPermissionsContext.Provider>
    );

    const updateSeverityButton = screen.getByRole("button", {
      name: "searchFindings.tabDescription.updateVulnSeverityButton",
    });

    expect(updateSeverityButton).toBeInTheDocument();
    expect(updateSeverityButton).toBeEnabled();

    await userEvent.click(updateSeverityButton);
    await waitFor((): void => {
      expect(onUpdateSeverity).toHaveBeenCalledTimes(1);
    });
  });
});
