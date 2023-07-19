import styled from "styled-components";

const CardFooter = styled.div`
  margin-top: auto;
`;

const CardLink = styled.div`
  height: 100%;
  padding: 42px 40px 40px;

  &:hover > #link {
    color: #bf0b1a;
    text-decoration-color: #bf0b1a;

    p {
      color: #bf0b1a;
      margin-right: 3px;
    }
  }
`;

export { CardFooter, CardLink };
