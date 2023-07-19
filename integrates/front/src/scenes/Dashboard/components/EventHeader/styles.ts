import styled from "styled-components";

const HeaderContainer = styled.div`
  background-color: #f4f4f6;
`;

const EventHeaderGrid = styled.div.attrs({
  className: "grid ma4 menu-grid",
})``;

const EventHeaderLabel = styled.div.attrs({
  className: "ph3 tc",
})``;

export { EventHeaderGrid, EventHeaderLabel, HeaderContainer };
