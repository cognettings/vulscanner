// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "Fluid Attacks Documentation",
  tagline: "Here you can find documentation for all our products",
  url: "https://docs.fluidattacks.com",
  baseUrl: process.env.env == "prod" ? "/" : `/${process.env.branch}/`,
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "throw",
  favicon:
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1677159785/docs/favicon-2023.png",

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebar.js"),
          routeBasePath: "/",
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      matomo: {
        matomoUrl: "https://fluidattacks.matomo.cloud/",
        siteId: "2",
      },
      colorMode: {
        defaultMode: "light",
        disableSwitch: false,
      },
      navbar: {
        logo: {
          alt: "Fluid Attacks Logo",
          src: "https://res.cloudinary.com/fluid-attacks/image/upload/v1675273694/docs/Logo_2023.svg",
          srcDark:
            "https://res.cloudinary.com/fluid-attacks/image/upload/v1675273694/docs/Logo_2023_dark.svg",
        },
        items: [
          {
            to: "about/",
            activeBasePath: "about/",
            label: "About",
            position: "left",
          },
          {
            to: "tech/",
            activeBasePath: "tech/",
            label: "Technology",
            position: "left",
          },
          {
            to: "plans/",
            activeBasePath: "plans/",
            label: "Plans",
            position: "left",
          },
          {
            to: "criteria/",
            activeBasePath: "criteria/",
            label: "Criteria",
            position: "left",
          },
          {
            to: "development/",
            activeBasePath: "development/",
            label: "Development",
            position: "right",
          },
          {
            to: "talent/",
            activeBasePath: "talent/",
            label: "Talent",
            position: "right",
          },
          {
            type: "html",
            position: "right",
            value:
              '<a target="_blank" rel="noopener noreferrer" href="https://app.fluidattacks.com/SignUp"><button class="trial-button">Start your free trial</button></a>',
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Community",
            items: [
              {
                label: "Help",
                href: "https://help.fluidattacks.tech",
              },
              {
                label: "LinkedIn",
                href: "https://www.linkedin.com/company/fluidattacks",
              },
              {
                label: "Ethics Hotline",
                href: "https://speakup.fluidattacks.tech/contactform/mail",
              },
            ],
          },
          {
            title: "Main",
            items: [
              {
                label: "Platform",
                to: "https://app.fluidattacks.com",
              },
              {
                label: "Website",
                to: "https://fluidattacks.com",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "Blog",
                to: "https://fluidattacks.com/blog",
              },
              {
                label: "Gitlab",
                href: "https://gitlab.com/fluidattacks/universe",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Fluid Attacks, We hack your software. All rights reserved.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: [
          "csharp",
          "java",
          "python",
          "typescript",
          "erlang",
          "javascript",
          "kotlin",
          "javascript",
          "php",
          "scala",
          "typescript",
          "ruby",
          "typescript",
          "dart",
          "elixir",
        ],
      },
    }),
  plugins: [
    [require.resolve("docusaurus-gtm-plugin"), { id: "GTM-PCDDL8T" }],
    require.resolve("docusaurus-lunr-search"),
    require.resolve("docusaurus-plugin-matomo"),
  ],
};

module.exports = config;
