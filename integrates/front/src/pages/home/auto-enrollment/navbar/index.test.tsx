import { render, screen } from "@testing-library/react";
import React from "react";
import { MemoryRouter } from "react-router-dom";

import { NavBar } from "pages/home/auto-enrollment/navbar";

describe("NavBar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof NavBar).toBe("function");
  });

  it("should render a NavBar", (): void => {
    expect.hasAssertions();

    render(
      <MemoryRouter initialEntries={["/home"]}>
        <NavBar progressWidth={0} userName={"John Doe"} />
      </MemoryRouter>
    );

    expect(screen.queryByRole("link")).toBeInTheDocument();
    expect(screen.getByRole("link")).toHaveAttribute("href", "/home");
    expect(screen.getByText("J")).toBeInTheDocument();
    expect(screen.getByText("Hi John!")).toBeInTheDocument();
  });
});
