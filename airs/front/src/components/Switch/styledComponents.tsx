import styled from "styled-components";

const SwitcherWrapper = styled.div`
  border: solid 1px #dddde3;
  border-radius: 6px;
  width: fit-content;
  max-height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const SwitcherButton = styled.button<{ active: boolean }>`
  margin-top: 8px;
  margin-bottom: 8px;
  margin-left: 12px;
  margin-right: 12px;
  background-color: ${(props): string =>
    props.active ? "#ffffff" : "transparent"};
  box-shadow: ${(props): string =>
    props.active ? "0 3px 6px 0 rgba(0, 0, 0, 0.16)" : ""};
  color: black;
  border-radius: 5px;
  border-top: none;
  border-left: none;
  border-right: none;
  border-bottom: ${(props): string =>
    props.active ? "3px solid #bf0b1a" : "none"};
  cursor: pointer;
  height: 32px;
  :hover {
    background-color: ${(props): string =>
      props.active ? "#ffffff" : "#f4f4f6"};
  }
`;

export { SwitcherButton, SwitcherWrapper };
