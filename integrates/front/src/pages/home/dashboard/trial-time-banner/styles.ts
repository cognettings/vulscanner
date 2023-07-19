import styled from "styled-components";

const ArrowContainer = styled.div`
  p {
    transition: background-color 0.1s;
  }

  :hover {
    p {
      color: #fda6ab !important;
    }

    a {
      color: #fda6ab !important;
    }

    svg {
      margin-left: 2px;
    }
  }
`;

export { ArrowContainer };
