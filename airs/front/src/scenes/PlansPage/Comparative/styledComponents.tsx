import styled from "styled-components";

const TableContainer = styled.div.attrs({
  className: `
  `,
})`
  box-shadow: 0 12px 24px 0 rgba(0, 0, 0, 0.12);
  border-radius: 5px;
  border: solid 1px #dddde3;
  max-width: 1431px;
  overflow-x: auto;
  padding-left: 40px;
  padding-right: 40px;
  width: 80%;
  ::-webkit-scrollbar {
    width: 3px;
    border-radius: 15px;
  }

  ::-webkit-scrollbar-track {
    background: #e9e9ed;
  }

  ::-webkit-scrollbar-thumb {
    background: #d2d2da;
  }
`;

const ComparativeTable = styled.table.attrs({
  className: `
  mv4
  w-100
  `,
})`
  border-collapse: collapse;
  @media (max-width: 800px) {
    min-width: 725px;
  }

  th:first-child {
    width: 50%;
  }
`;

const HeadColumn = styled.th`
  border-bottom: solid 1px #2e2e38;
  height: 123px;
  align-items: center;
`;

const Row = styled.tr`
  border-bottom: solid 1px #dddde3;
  height: 64px;
`;

const Cell = styled.td`
  text-align: center;
`;
const DescriptionCell = styled.td`
  color: #535365;
  font-size: 16px;
  padding-left: 16px;
`;

export {
  ComparativeTable,
  HeadColumn,
  Row,
  TableContainer,
  Cell,
  DescriptionCell,
};
