import styled from "styled-components";

const ProgressBar = styled.div<{ width: string }>`
  position: relative;
  background-color: #bf0b1a;
  height: 100%;
  width: ${({ width }): string => width};
  transition: width 0.25s;
`;

export { ProgressBar };
