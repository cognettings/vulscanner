import { fireEvent, render } from "@testing-library/react";
import React from "react";

import { SortDropdown } from "components/SortDropdown";

describe("Sort Dropdown", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof SortDropdown).toBe("function");
  });

  it("test clicking option updates sort value and direction", (): void => {
    expect.hasAssertions();

    const onChangeMock = jest.fn();
    const mappedOptions = [
      { header: "Option 1", value: "option1" },
      { header: "Option 2", value: "option2" },
    ];
    const { getAllByText, getByRole } = render(
      <SortDropdown
        id={"sortDropdown"}
        mappedOptions={mappedOptions}
        onChange={onChangeMock}
      />
    );
    const option1Button = getByRole("button", { name: "Option 1" });
    fireEvent.click(option1Button);

    expect(getAllByText("Option 1")[0]).toBeInTheDocument();
    expect(option1Button.querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "arrow-down-wide-short"
    );
    expect(onChangeMock).toHaveBeenCalledWith("option1", "DESC");

    fireEvent.click(option1Button);

    expect(option1Button.querySelector(".svg-inline--fa")).toHaveAttribute(
      "data-icon",
      "arrow-down-short-wide"
    );
    expect(onChangeMock).toHaveBeenCalledWith("option1", "ASC");
  });

  it("test on change called with correct parameters", (): void => {
    expect.hasAssertions();

    const onChangeMock = jest.fn();
    const mappedOptions = [
      { header: "Option 1", value: "option1" },
      { header: "Option 2", value: "option2" },
    ];
    const { getByText, getAllByText } = render(
      <SortDropdown
        id={"sortDropdown"}
        mappedOptions={mappedOptions}
        onChange={onChangeMock}
      />
    );
    const button = getAllByText("Option 1");
    fireEvent.click(button[0]);
    const option = getByText("Option 2");
    fireEvent.click(option);

    expect(onChangeMock).toHaveBeenCalledTimes(3);
    expect(onChangeMock).toHaveBeenCalledWith("option2", "ASC");
  });

  it("test mapped options empty", (): void => {
    expect.hasAssertions();

    const onChangeMock = jest.fn();
    const { getByRole } = render(
      <SortDropdown id={"sortDropdown"} onChange={onChangeMock} />
    );
    const sortButton = getByRole("button");

    expect(sortButton.textContent).toBe("");
  });

  it("test mapped options has only one option", (): void => {
    expect.hasAssertions();

    const onChange = jest.fn();
    const mappedOptions = [{ header: "Option 1", value: "option1" }];
    const { getAllByRole } = render(
      <SortDropdown
        id={"sortDropdown"}
        mappedOptions={mappedOptions}
        onChange={onChange}
      />
    );
    const sortButton = getAllByRole("button");

    expect(sortButton).toHaveLength(mappedOptions.length);
  });
});
