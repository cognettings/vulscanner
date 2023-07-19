/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IContentSwitcherProps } from ".";
import { ContentSwitcher } from ".";

const config: Meta = {
  component: ContentSwitcher,
  tags: ["autodocs"],
  title: "components/ContentSwitcher",
};

const Template: Story<IContentSwitcherProps> = (props): JSX.Element => (
  <ContentSwitcher {...props} />
);

const Default = Template.bind({});
Default.args = {
  contents: [...Array(4).keys()].map(
    (el: number): JSX.Element => <p key={el}>{`Content ${el}`}</p>
  ),
  tabs: ["Analytics", "Groups", "Portfolios", "Policies"],
};

export { Default };
export default config;
