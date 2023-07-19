import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

import { StepLapse } from ".";
import { Text } from "../Text";

const functionMock: () => void = (): void => undefined;

describe("Step lapse", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof StepLapse).toBe("function");
  });

  it("should render a step lapse", async (): Promise<void> => {
    expect.hasAssertions();

    render(
      <StepLapse
        finalButtonText={"Send"}
        finalClick={functionMock}
        isDisabledFinalButton={true}
        steps={[
          {
            content: (
              <div>
                <Text>{"I'am first step"}</Text>
              </div>
            ),
            title: "First step",
          },
          {
            content: (
              <div>
                <Text>{"I'am"}</Text>
                <Text>{"second"}</Text>
                <Text>{"step"}</Text>
              </div>
            ),
            title: "Second step",
          },
          {
            content: (
              <div>
                <Text>{"I'am third step"}</Text>
              </div>
            ),
            title: "Third step",
          },
        ]}
      />
    );

    expect(screen.getByText("First step")).toBeInTheDocument();
    expect(screen.getByText("Second step")).toBeInTheDocument();
    expect(screen.getByText("Third step")).toBeInTheDocument();
    expect(screen.getByText("I'am first step")).toBeInTheDocument();

    expect(screen.queryAllByRole("button")).toHaveLength(1);

    await userEvent.click(screen.getAllByRole("button")[0]);

    expect(screen.getByText("I'am")).toBeInTheDocument();
    expect(screen.getByText("second")).toBeInTheDocument();
    expect(screen.getByText("step")).toBeInTheDocument();

    expect(screen.queryAllByRole("button")).toHaveLength(2);

    await userEvent.click(screen.getAllByRole("button")[1]);

    expect(screen.getByText("I'am third step")).toBeInTheDocument();
    expect(screen.getByText("Send")).toBeInTheDocument();

    expect(screen.queryAllByRole("button")).toHaveLength(2);

    await userEvent.click(screen.getAllByRole("button")[0]);
    await userEvent.click(screen.getAllByRole("button")[0]);

    expect(screen.getByText("I'am first step")).toBeInTheDocument();
  });
});
