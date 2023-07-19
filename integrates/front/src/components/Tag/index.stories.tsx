/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { ITagProps } from ".";
import { Tag } from ".";

const config: Meta = {
  component: Tag,
  tags: ["autodocs"],
  title: "components/Tag",
};

const Template: Story<React.PropsWithChildren<ITagProps>> = (
  props
): JSX.Element => <Tag {...props} />;

const Default = Template.bind({});
Default.args = {
  children: "Test",
  variant: "green",
};

export { Default };
export default config;
