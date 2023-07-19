import { Link } from "gatsby";
import styled from "styled-components";

import type { ILinkProps } from "./types";

const ExternalLink = styled.a<ILinkProps>`
  ${({ decoration = "underline", hovercolor = "" }): string => `
    color: inherit;
    text-decoration: ${decoration};
    text-decoration-color: inherit;

    :hover {
      color: ${hovercolor ? `${hovercolor}` : "inherit"};
      text-decoration-color: ${hovercolor ? `${hovercolor}` : "inherit"};

      p {
        color: ${hovercolor ? `${hovercolor}` : "inherit"};
      }
    }
  `}
`;

const InternalLink = styled(Link)<ILinkProps>`
  ${({ decoration = "none", hovercolor = "" }): string => `
    color: inherit;
    text-decoration: ${decoration};
    text-decoration-color: inherit;

    :hover {
      color: ${hovercolor ? `${hovercolor}` : "inherit"};
      text-decoration-color: ${hovercolor ? `${hovercolor}` : "inherit"};

      p {
        color: ${hovercolor ? `${hovercolor}` : "inherit"};
      }
    }
  `}
`;

export { ExternalLink, InternalLink };
