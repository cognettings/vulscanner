import styled from "styled-components";

import type { ExternalLinkProps } from "./types";

const ExternalLinkOutline = styled.a.attrs<ExternalLinkProps>({
  className: "comp-ext-link-out f6 link dib",
  // https://owasp.org/www-community/attacks/Reverse_Tabnabbing
  rel: "nofollow noopener noreferrer",
  target: "_blank",
})`
  border-radius: 4px;
  color: inherit;
  padding: 6px;
  text-decoration: underline;
  text-underline-offset: 5px;
  background-color: transparent;
  transition: background-color 0.1s;
  :hover {
    color: #5c5c70;
    text-decoration: underline;
  }
`;

export { ExternalLinkOutline };
