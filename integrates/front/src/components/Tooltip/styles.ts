import styled from "styled-components";

type TPlace = "bottom" | "left" | "right" | "top";

interface ITooltipBoxAttrs {
  className: string;
  "data-for": string;
  "data-effect": string;
  "data-html": boolean;
  "data-place": TPlace;
  "data-tip": string;
}

interface ITooltipBoxProps {
  disp?: "block" | "flex" | "inline-block" | "inline";
  id: string;
  effect?: "float" | "solid";
  place?: TPlace;
  tip?: string;
}

const TooltipBox = styled.div.attrs(
  ({
    id,
    effect = "solid",
    place = "bottom",
    tip = "",
  }: ITooltipBoxProps): ITooltipBoxAttrs => ({
    className: "comp-tooltip",
    "data-effect": effect,
    "data-for": id,
    "data-html": true,
    "data-place": place,
    "data-tip": tip,
  })
)<ITooltipBoxProps>`
  ${({ disp = "block" }): string => `
  display: ${disp};

  > .__react_component_tooltip {
    opacity: 0.7;
    padding: 5px;
    text-align: center;
    white-space: pre-line;
    width: 300px;
    z-index: 10000;
  }
  `}
`;

export type { ITooltipBoxProps, TPlace };
export { TooltipBox };
