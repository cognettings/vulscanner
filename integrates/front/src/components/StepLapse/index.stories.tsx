/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import type { PropsWithChildren } from "react";
import React from "react";

import type { IStepLapseProps } from "./types";

import { StepLapse } from ".";

const config: Meta = {
  component: StepLapse,
  tags: ["autodocs"],
  title: "components/StepLapse",
};

const Template: Story<PropsWithChildren<IStepLapseProps>> = (
  props
): JSX.Element => <StepLapse {...props} />;

const Default = Template.bind({});
Default.args = {
  finalButtonText: "Send",
  finalClick: (): void => undefined,
  isDisabledFinalButton: true,
  steps: [
    {
      content: (
        <div>
          <p>{"I'am first step"}</p>
        </div>
      ),
      title: "First step",
    },
    {
      content: (
        <div>
          <p>{"I'am"}</p>
          <p>{"second"}</p>
          <p>{"step"}</p>
        </div>
      ),
      title: "Second step",
    },
    {
      content: (
        <div>
          <p>{"I'am third step"}</p>
        </div>
      ),
      title: "Third step",
    },
  ],
};

export { Default };
export default config;
