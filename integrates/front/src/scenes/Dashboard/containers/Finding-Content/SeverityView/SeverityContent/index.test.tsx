import { render, screen } from "@testing-library/react";
import _ from "lodash";
import React from "react";

import { SeverityTile } from "./tile";

import { userInteractionBgColors } from "../utils";
import { userInteractionValues } from "utils/cvss";

describe("SeverityTile", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SeverityTile).toBe("function");
  });

  it("should render a tile", (): void => {
    expect.hasAssertions();

    render(
      <SeverityTile
        color={userInteractionBgColors.N}
        name={"userInteraction"}
        valueText={userInteractionValues.N}
      />
    );

    expect(
      screen.queryByText(_.capitalize(userInteractionValues.N))
    ).toBeInTheDocument();
  });
});
