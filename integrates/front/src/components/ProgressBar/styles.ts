/* eslint-disable @typescript-eslint/no-magic-numbers */
import styled from "styled-components";

interface IBarProps {
  color?: string;
  display?: string;
  height?: number;
  leftRadius?: number;
  rightRadius?: number;
  maxWidth?: number;
  minWidth?: number;
  widthPercentage?: number;
}

const Bar = styled.div<IBarProps>`
  ${({
    color = "red",
    display = "block",
    height = 25,
    leftRadius = 0,
    rightRadius = 0,
    maxWidth = 500,
    minWidth = 0,
    widthPercentage = 100,
  }): string => `
    display: ${display};
    background-color: ${color};
    width:${widthPercentage}%;
    max-width:${maxWidth}px;
    min-width:${minWidth}px;
    height:${height}px;
    border-radius: ${leftRadius}px ${rightRadius}px ${rightRadius}px ${leftRadius}px;
  `}
`;

export type { IBarProps };
export { Bar };
