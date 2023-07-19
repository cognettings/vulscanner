/* eslint-disable react/forbid-component-props */

import "tachyons";
import { Parameters } from "@storybook/api";
import { DocsPage } from "./DocsPage";

const parameters: Parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  docs: {
    page: DocsPage,
    source: {
      state: "open",
      type: "dynamic",
    },
  },
  viewMode: "docs",
};

export { parameters };
