/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React from "react";

import type { IHeroProps } from "./types";

import { Hero } from ".";

const config: Meta = {
  component: Hero,
  title: "components/Hero",
};

const Template: Story<React.PropsWithChildren<IHeroProps>> = (
  props
): JSX.Element => <Hero {...props} />;

const Default = Template.bind({});
Default.args = {
  button1Link: "/test/",
  button1Text: "Go to test",
  button2Link: "/other-test/",
  button2Text: "Go to other test",
  image: "/airs/home/HeaderHero/hero-image.png",
  matomoAction: "Test",
  paragraph:
    "This is a test paragraph that should show the behavior of the Hero",
  subtitle: "Test subtitle",
  title: "This is a test title",
};

export { Default };
export default config;
