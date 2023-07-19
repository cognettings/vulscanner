import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { HandleAcceptanceButton } from ".";
import { authzPermissionsContext } from "context/authz/config";

describe("HandleAcceptanceButtons", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof HandleAcceptanceButton).toBe("function");
  });

  it("should render a component", async (): Promise<void> => {
    expect.hasAssertions();

    const openHandleAcceptance: jest.Mock = jest.fn();
    const handleAcceptanceButtonText: string =
      "searchFindings.tabVuln.buttons.handleAcceptance";
    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_handle_vulnerabilities_acceptance_mutate" },
    ]);
    const { rerender } = render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <HandleAcceptanceButton
          areRequestedZeroRiskVulns={true}
          areSubmittedVulns={true}
          areVulnsPendingOfAcceptance={true}
          isClosing={false}
          isEditing={true}
          isRequestingReattack={false}
          isResubmitting={false}
          isVerifying={false}
          openHandleAcceptance={openHandleAcceptance}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByText(handleAcceptanceButtonText)).toHaveLength(0);

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <HandleAcceptanceButton
          areRequestedZeroRiskVulns={false}
          areSubmittedVulns={false}
          areVulnsPendingOfAcceptance={false}
          isClosing={false}
          isEditing={false}
          isRequestingReattack={false}
          isResubmitting={false}
          isVerifying={false}
          openHandleAcceptance={openHandleAcceptance}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryAllByText(handleAcceptanceButtonText)).toHaveLength(0);

    rerender(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <HandleAcceptanceButton
          areRequestedZeroRiskVulns={true}
          areSubmittedVulns={true}
          areVulnsPendingOfAcceptance={true}
          isClosing={false}
          isEditing={false}
          isRequestingReattack={false}
          isResubmitting={false}
          isVerifying={false}
          openHandleAcceptance={openHandleAcceptance}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.getByText(handleAcceptanceButtonText)).toBeInTheDocument();

    await userEvent.click(screen.getByText(handleAcceptanceButtonText));

    expect(openHandleAcceptance).toHaveBeenCalledTimes(1);
  });
});
