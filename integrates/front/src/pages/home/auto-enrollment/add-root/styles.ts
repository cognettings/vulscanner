import styled from "styled-components";

const QuestionButton = styled.button.attrs(
  ({ type }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `outline-0 pa0`,
    type: type ?? "button",
  })
)`
  border: 0 !important;
  color: #bf0b1a;

  :hover {
    background-color: unset !important;
    color: #272727 !important;
  }
`;

export { QuestionButton };
