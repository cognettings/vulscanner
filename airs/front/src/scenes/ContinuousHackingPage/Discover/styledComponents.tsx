import styled from "styled-components";

const ContinuousRow = styled.article`
  width: 100%;
  max-width: 1440px;
  :after {
    content: "";
    display: table;
    clear: both;
  }
  @media screen and (max-width: 1140px) {
    margin-left: 48px;
    margin-right: 48px;
  }
`;

const ContentColumn = styled.div`
  float: left;
  width: 45%;
  padding: 20px;
`;

const VectorColumn = styled.div`
  float: left;
  width: 10%;
  padding: 10px;
`;

export { VectorColumn, ContentColumn, ContinuousRow };
