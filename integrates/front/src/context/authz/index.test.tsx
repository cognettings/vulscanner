import { render, screen } from "@testing-library/react";
import React from "react";

import { Can } from "context/authz/Can";
import {
  authzGroupContext,
  authzPermissionsContext,
  groupAttributes,
  userLevelPermissions,
} from "context/authz/config";
import { Have } from "context/authz/Have";

describe("Authorization", (): void => {
  it("should return functions", (): void => {
    expect.hasAssertions();

    expect(typeof Can).toBe("function");
    expect(typeof Have).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    userLevelPermissions.update([{ action: "resolve_hacker" }]);
    render(
      <authzPermissionsContext.Provider value={userLevelPermissions}>
        <Can do={"resolve_hacker"}>
          <p>{"someone@fluidattacks.com"}</p>
        </Can>
      </authzPermissionsContext.Provider>
    );

    expect(screen.queryByText("someone@fluidattacks.com")).toBeInTheDocument();
  });

  it("should render Have", (): void => {
    expect.hasAssertions();

    groupAttributes.update([{ action: "has_asm" }]);

    render(
      <authzGroupContext.Provider value={groupAttributes}>
        <Have I={"has_asm"}>
          <p>{"I have ASM"}</p>
        </Have>
      </authzGroupContext.Provider>
    );

    expect(screen.queryByText("I have ASM")).toBeInTheDocument();
  });

  it("should not render", (): void => {
    expect.hasAssertions();

    userLevelPermissions.update([]);
    render(
      <authzPermissionsContext.Provider value={userLevelPermissions}>
        <Can do={"resolve_hacker"}>
          <p>{"someone@fluidattacks.com"}</p>
        </Can>
      </authzPermissionsContext.Provider>
    );

    expect(
      screen.queryByText("someone@fluidattacks.com")
    ).not.toBeInTheDocument();
  });

  it("should not render Have", (): void => {
    expect.hasAssertions();

    groupAttributes.update([]);

    render(
      <authzGroupContext.Provider value={groupAttributes}>
        <Have I={"has_asm"}>
          <p>{"I have ASM"}</p>
        </Have>
      </authzGroupContext.Provider>
    );

    expect(screen.queryByText("I have ASM")).not.toBeInTheDocument();
  });
});
