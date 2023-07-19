import { render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { MemoryRouter, Route } from "react-router-dom";

import { OrganizationPortfolios } from "scenes/Dashboard/containers/Organization-Content/OrganizationPortfoliosView";
import type { IPortfolios } from "scenes/Dashboard/containers/Organization-Content/OrganizationPortfoliosView/types";

describe("Portfolios info is rendered", (): void => {
  const portfoliosInfo: IPortfolios[] = [
    {
      groups: [
        {
          name: "continuoustesting",
        },
        {
          name: "oneshottest",
        },
      ],
      name: "front testing",
    },
    {
      groups: [
        {
          name: "continuoustesting",
        },
        {
          name: "unittesting",
        },
        {
          name: "oneshottest",
        },
      ],
      name: "test-groups",
    },
  ];

  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof OrganizationPortfolios).toBe("function");
  });

  it("should render table columns", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/portfolios"]}>
        <Route path={"/portfolios"}>
          <OrganizationPortfolios portfolios={portfoliosInfo} />
        </Route>
      </MemoryRouter>
    );

    expect(screen.queryAllByRole("table")).toHaveLength(1);
    expect(screen.getByText("Portfolio")).toBeInTheDocument();
    expect(screen.getByText("# of Groups")).toBeInTheDocument();
    expect(screen.getByText("Groups")).toBeInTheDocument();

    await waitFor((): void => {
      expect(screen.queryByText("front testing")).toBeInTheDocument();
    });

    expect(screen.getByText("2")).toBeInTheDocument();
    expect(
      screen.getByText("continuoustesting, oneshottest")
    ).toBeInTheDocument();
    expect(screen.getByText("test-groups")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
    expect(
      screen.getByText("continuoustesting, unittesting, oneshottest")
    ).toBeInTheDocument();
  });
});
