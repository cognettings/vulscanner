/* eslint-disable import/no-default-export */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import { Timeline } from ".";
import { Card } from "components/Card";
import { Text } from "components/Text";

const config: Meta = {
  component: Timeline,
  tags: ["autodocs"],
  title: "components/Timeline",
};

const Default: Story = (): JSX.Element => (
  <Timeline>
    {[23, 24, 25, 26].map(
      (el: number): JSX.Element => (
        <Card float={true} key={el} title={`2022-07-${el}`}>
          <Text fw={7} mb={1} size={"big"}>
            {"Lorem ipsum"}
          </Text>
          <Text>
            {"Lorem ipsum dolor sit amet, consectetur adipiscing elit."}
          </Text>
        </Card>
      )
    )}
  </Timeline>
);

export { Default };
export default config;
