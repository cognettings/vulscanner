import { MockedProvider } from "@apollo/client/testing";
import { render, waitFor } from "@testing-library/react";
import React from "react";

import { ChartsView } from "scenes/Dashboard/components/ChartsGenericView";

describe("ChartsGenericView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsView).toBe("function");
  });

  it("should render a component and number of graphics of entity", async (): Promise<void> => {
    expect.hasAssertions();

    const groupGraphics: number = 39;
    const organizationAndPortfolioGraphics: number = 44;

    const { container, rerender } = render(
      <MockedProvider addTypename={true} mocks={[]}>
        <ChartsView
          bgChange={false}
          entity={"organization"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        organizationAndPortfolioGraphics
      );
    });

    rerender(
      <MockedProvider addTypename={true} mocks={[]}>
        <ChartsView
          bgChange={false}
          entity={"group"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );

    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        groupGraphics
      );
    });

    rerender(
      <MockedProvider addTypename={true} mocks={[]}>
        <ChartsView
          bgChange={false}
          entity={"portfolio"}
          reportMode={false}
          subject={"subject"}
        />
      </MockedProvider>
    );
    await waitFor((): void => {
      expect(container.getElementsByClassName("frame")).toHaveLength(
        organizationAndPortfolioGraphics
      );
    });
  });
});
