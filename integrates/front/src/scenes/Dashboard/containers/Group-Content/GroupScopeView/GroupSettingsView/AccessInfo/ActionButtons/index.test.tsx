import { PureAbility } from "@casl/ability";
import { render, screen } from "@testing-library/react";
import React from "react";

import { authzPermissionsContext } from "context/authz/config";
import { ActionButtons } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/ActionButtons";
import type { IActionButtonsProps } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/AccessInfo/ActionButtons";

describe("ActionButtons", (): void => {
  const baseMockedProps: IActionButtonsProps = {
    editTooltip: "tooltip",
    isEditing: false,
    isPristine: false,
    onEdit: jest.fn(),
    onUpdate: jest.fn(),
    permission: "api_mutations_update_group_access_info_mutate",
  };

  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ActionButtons).toBe("function");
  });

  it("should render a component", (): void => {
    expect.hasAssertions();

    const mockedPermissions = new PureAbility<string>([
      { action: "api_mutations_update_group_access_info_mutate" },
    ]);
    const { editTooltip, isEditing, isPristine, onEdit, onUpdate, permission } =
      baseMockedProps;
    render(
      <authzPermissionsContext.Provider value={mockedPermissions}>
        <ActionButtons
          editTooltip={editTooltip}
          isEditing={isEditing}
          isPristine={isPristine}
          onEdit={onEdit}
          onUpdate={onUpdate}
          permission={permission}
        />
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByRole("button")).toBeInTheDocument();
    expect(
      screen.queryByText("searchFindings.tabDescription.editable.text")
    ).toBeInTheDocument();
  });
});
