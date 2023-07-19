import {
  ArgsTable,
  Description,
  DocsContext,
  DocsContextProps,
  PRIMARY_STORY,
  Primary,
  Source,
  Stories,
  Subtitle,
  Title,
} from "@storybook/addon-docs";
import { ReactFramework } from "@storybook/react";
import React, { Context, useContext } from "react";
import styled from "styled-components";

const ImportStatement = (): JSX.Element => {
  const context = useContext(
    DocsContext as Context<DocsContextProps<ReactFramework>>
  );
  const defaultStory = context.componentStories()[0];
  const component = defaultStory.component?.displayName;
  const subcomponents = Object.keys(defaultStory.subcomponents ?? {});
  const components = [component, ...subcomponents]
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b))
    .join(", ");
  const path = context.title;
  const statement = `import { ${components} } from "${path}"`;

  return <Source dark={true} language={"js"} code={statement} />;
};

const SBDocsTheme = styled.div.attrs({
  className: "sb-theme",
})`
  font-family: Poppins, sans-serif;
`;

const DocsPage = (): JSX.Element => (
  <SBDocsTheme>
    <Title />
    <Subtitle />
    <Description />
    <ImportStatement />
    <Primary />
    <ArgsTable story={PRIMARY_STORY} />
    <Stories />
  </SBDocsTheme>
);

export { DocsPage };
