import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const LanguagesListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  mw-1366
  ph-body
  center
  pv5
  v-top
  mb5
  poppins
`,
})``;

const ListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  center
  mw8
  tc
`,
})``;

const ListColumn: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
  list
  poppins
  f5
  dib-l
  ph4
  mv0
  pv0-l
  pv4
  tl
`,
})`
  color: #5c5c70;
`;

const SastParagraph: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    center
    poppins
    f3-l
    f4
    lh-2
    pv4
    tc
  `,
})``;

export { LanguagesListContainer, ListColumn, ListContainer, SastParagraph };
