import styled from "styled-components";

const ButtonToolbarCenter = styled.div.attrs({
  className: "flex flex-wrap justify-center pv3 w-100",
})``;

const ButtonToolbarStartRow = styled.div.attrs({
  className: "flex flex-wrap items-center justify-start",
})``;

const ButtonToolbarRow = styled.div.attrs({
  className: "flex flex-wrap items-center justify-end",
})``;

export { ButtonToolbarCenter, ButtonToolbarStartRow, ButtonToolbarRow };
