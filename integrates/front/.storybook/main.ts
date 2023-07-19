import type { StorybookConfig } from "@storybook/react-vite";
import { mergeConfig } from "vite";
import { commonConfig as viteConfig } from "../vite.common.config";

const config: StorybookConfig = {
  core: { builder: "@storybook/builder-vite" },
  stories: ["../src/**/*.stories.mdx", "../src/**/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",
    "@storybook/addon-a11y",
    "@storybook/addon-links",
    "@storybook/addon-interactions",
  ],
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  docs: {
    autodocs: "tag",
  },
  viteFinal: async (config) => {
    return mergeConfig(config,
      {
        build:{
          minify: false,
          sourcemap: false,
        },
        resolve: {
          alias: {
            ...viteConfig.resolve.alias,
          },
        },
      });
  },
};
export default config;
