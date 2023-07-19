/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";
import type { PropsWithChildren } from "react";

import type { IInfoDropdownProps } from ".";
import { InfoDropdown } from ".";

const config: Meta = {
  component: InfoDropdown,
  tags: ["autodocs"],
  title: "components/InfoDropdown",
};

const Template: Story<PropsWithChildren<IInfoDropdownProps>> = (
  props
): JSX.Element => <InfoDropdown {...props}>{"Information"}</InfoDropdown>;

const Default = Template.bind({});
Default.args = {
  alignDropdown: "right",
  size: "small",
};

export { Default };
export default config;
