import styled from "styled-components";

const BreadcrumbContainer = styled.div.attrs({
  className: "breadcrumb list",
})``;

const NavSplitButtonContainer = styled.div.attrs({
  className: "split-button",
})`
  padding-right: 24px;
`;

const SplitItems = styled.div.attrs({
  className: "mr3 pb2 flex flex-wrap fixed br2",
})`
  background-color: #f4f4f6;
  border: solid 1px;
  border-color: #ddd;
  box-shadow: 0 8px 16px 0 rgb(0 0 0 / 20%);
  color: #333;
  margin-top: 5px;
  max-width: 1172px;
  max-height: 835px;
  overflow: auto;
  writing-mode: vertical-lr;
  z-index: 1;

  @media (max-width: 1297px) {
    max-width: 1055px;
  }

  @media (max-width: 1180px) {
    max-width: 938px;
  }

  @media (max-width: 1063px) {
    max-width: 821px;
  }

  @media (max-width: 946px) {
    max-width: 704px;
  }

  @media (max-width: 829px) {
    max-width: 587px;
  }

  @media (max-width: 712px) {
    max-width: 470px;
  }

  @media (max-width: 595px) {
    max-width: 353px;
  }

  @media (max-width: 478px) {
    max-width: 236px;
  }

  @media (max-width: 361px) {
    max-width: 119px;
  }
`;

const StyledMenuItem = styled.span.attrs(
  ({ className }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `black bn br0 f5 inline-flex items-center mh3 outline-0 pa0 tl pointer bg-transparent ${
      className ?? ""
    }`,
  })
)`
  height: 55px;
  width: 85px;
  writing-mode: horizontal-tb;
  border-bottom: 1px solid #e5e5e5 !important;

  :hover {
    color: #bf0b1a;
  }
`;

export {
  BreadcrumbContainer,
  NavSplitButtonContainer,
  SplitItems,
  StyledMenuItem,
};
