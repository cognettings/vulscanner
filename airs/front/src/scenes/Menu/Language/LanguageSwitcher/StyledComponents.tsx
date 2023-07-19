import styled from "styled-components";

const Switcher = styled.div`
  width: max-content;
  height: 30px;
  background-color: transparent;
  border-radius: 4px;
  font-size: 14px;
  color: #2e2e38;
  outline: none;
  box-sizing: border-box;
  margin-left: 12px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  z-index: 999999999;

  > svg {
    padding-left: 2px;
    padding-right: 5px;
  }

  :hover {
    background-color: #dddde3;
  }
`;
const LanguagesContainer = styled.div.attrs({})<{ isShown: boolean }>`
  display: ${({ isShown }): string => (isShown ? "flex" : "none")};
  flex-wrap: wrap;
  height: 60px;
  border-radius: 5px;
  font-size: 14px;
  max-width: 97px;
  margin-left: 8px;
  background-color: #ffffff;
  border: 1px solid #dddde3;
  width: 100%;
  left: 0%;
  top: 100%;
  position: absolute;
  z-index: 999999999;

  > div {
    :hover {
      color: #bf0b1a;
    }
  }
`;

const LanguagesButton = styled.button`
  color: #535365;
  display: flex;
  padding: 0px;
  padding-left: 5px;
  align-items: center;
  background-color: transparent;
  border: none;
  justify-content: center;
  width: 100%;
  :hover {
    background-color: #dddde3;
  }
  :disabled {
    :hover {
      background-color: transparent;
      color: #dddde3;
    }
    color: #dddde3;
  }
`;
export { LanguagesContainer, Switcher, LanguagesButton };
