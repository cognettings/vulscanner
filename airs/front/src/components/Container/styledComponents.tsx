import styled from "styled-components";

import type {
  IContainerProps,
  TAlign,
  TDirection,
  TDisplay,
  TJustify,
  TWrap,
} from "./types";

const aligns: Record<TAlign, string> = {
  center: "center",
  end: "end",
  start: "start",
  stretch: "stretch",
  unset: "unset",
};

const directions: Record<TDirection, string> = {
  column: "column",
  reverse: "row-reverse",
  row: "row",
  unset: "unset",
};

const displays: Record<TDisplay, string> = {
  block: "block",
  flex: "flex",
  ib: "inline-block",
  inline: "inline",
  none: "none",
};

const justifies: Record<TJustify, string> = {
  around: "space-around",
  between: "space-between",
  center: "center",
  end: "flex-end",
  start: "flex-start",
  unset: "unset",
};

const wraps: Record<TWrap, string> = {
  nowrap: "nowrap",
  unset: "unset",
  wrap: "wrap",
};

const getWidth = (defaultWidth: string, width?: string): string =>
  width === undefined ? `width: ${defaultWidth};` : `width: ${width};`;

const getMinWidth = (defaultWidth: string, width?: string): string =>
  width === undefined ? `min-width: ${defaultWidth};` : `min-width: ${width};`;

const getJustify = (defaultJustify: TJustify, justify?: TJustify): string =>
  justify === undefined
    ? `justify-content: ${justifies[defaultJustify]};`
    : `justify-content: ${justifies[justify]};`;

const getBorder = (
  borderColor?: string,
  borderBottomColor?: string,
  borderTopColor?: string,
  leftBar?: string,
  topBar?: string
): string => {
  if (borderColor !== undefined) {
    return `border: 1px solid ${borderColor};`;
  } else if (borderBottomColor !== undefined) {
    return `border-bottom: 1px solid ${borderBottomColor};`;
  } else if (borderTopColor !== undefined) {
    return `border-top: 1px solid ${borderTopColor};`;
  } else if (leftBar !== undefined) {
    return `border-left: 5px solid ${leftBar};`;
  } else if (topBar !== undefined) {
    return `border-top: 5px solid ${topBar};`;
  }

  return "";
};

const getHorizontalMargin = (
  center: boolean,
  mh: number,
  mr: number,
  ml: number
): string => {
  if (center) {
    return `center`;
  } else if (mh !== 0) {
    return `mh${mh}`;
  }

  return `mr${mr} ml${ml}`;
};

const getHorizontalPadding = (
  ph: number,
  phMd?: number,
  phSm?: number
): string => {
  if (phMd !== undefined && phSm !== undefined) {
    return `ph${ph}-l ph${phMd}-m ph${phSm}`;
  } else if (phMd !== undefined) {
    return `ph${ph}-l ph${phMd}`;
  } else if (phSm !== undefined) {
    return `ph${ph}-ns ph${phSm}`;
  }

  return `ph${ph}`;
};

const getVerticalPadding = (
  pv: number,
  pvMd?: number,
  pvSm?: number
): string => {
  if (pvMd !== undefined && pvSm !== undefined) {
    return `pv${pv}-l pv${pvMd}-m pv${pvSm}`;
  } else if (pvMd !== undefined) {
    return `pv${pv}-l pv${pvMd}`;
  } else if (pvSm !== undefined) {
    return `pv${pv}-ns pv${pvSm}`;
  }

  return `pv${pv}`;
};

const getMarginTop = (mt: number, mtMd?: number, mtSm?: number): string => {
  if (mtMd !== undefined && mtSm !== undefined) {
    return `mt${mt}-l mt${mtMd}-m mt${mtSm}`;
  } else if (mtMd !== undefined) {
    return `mt${mt}-l mt${mtMd}`;
  } else if (mtSm !== undefined) {
    return `mt${mt}-ns mt${mtSm}`;
  }

  return `mt${mt}`;
};

const getShadow = (shadow: boolean, shadowBottom?: boolean): string => {
  if (shadowBottom === true) {
    return "box-shadow: 0px 10px 7px -2px rgba(0,0,0,0.16);";
  } else if (shadow) {
    return "box-shadow: 0 10px 20px 0 rgba(0, 0, 0, 0.16);";
  }

  return "";
};

const StyledContainer = styled.div.attrs<IContainerProps>(
  ({
    br = 0,
    center = false,
    classname = "",
    mb = 0,
    mh = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    mtMd,
    mtSm,
    mv = 0,
    onClick,
    pb = 0,
    ph = 0,
    phMd,
    phSm,
    pl = 0,
    pr = 0,
    pt = 0,
    pv = 0,
    pvMd,
    pvSm,
  }): {
    className: string;
  } => ({
    className: `
      br${br === 100 ? "-100" : br}
      ${mv === 0 ? `mb${mb} ${getMarginTop(mt, mtMd, mtSm)}` : `mv${mv}`}
      ${getHorizontalMargin(center, mh, mr, ml)}
      ${
        pv === 0 && pvMd === undefined && pvSm === undefined
          ? `pb${pb} pt${pt}`
          : `${getVerticalPadding(pv, pvMd, pvSm)}`
      }
      ${
        ph === 0 && phMd === undefined && phSm === undefined
          ? `pl${pl} pr${pr}`
          : `${getHorizontalPadding(ph, phMd, phSm)}`
      }
      ${onClick ? "pointer" : ""}
      ${classname}
    `,
  })
)<IContainerProps>`
  ${({
    align = "unset",
    bgColor = "transparent",
    bgGradient,
    borderBottomColor,
    borderColor,
    borderTopColor,
    borderHoverColor,
    direction = "unset",
    display = "block",
    displayMd,
    displaySm,
    height = "auto",
    hovercolor = "",
    hoverShadow = false,
    justify = "unset",
    justifyMd,
    justifySm,
    leftBar,
    maxWidth = "100%",
    minHeight = "0",
    minWidth = "0",
    minWidthMd,
    minWidthSm,
    position = "unset",
    scroll = "none",
    shadow = false,
    shadowBottom = false,
    textHoverColor = "",
    topBar,
    width = "100%",
    widthMd,
    widthSm,
    wrap = "unset",
  }): string => `
    align-items: ${aligns[align]};
    background: ${
      bgGradient === undefined ? "" : `linear-gradient(${bgGradient})`
    };
    background-color: ${bgColor};
    display: ${displays[display]};
    flex-direction: ${directions[direction]};
    flex-wrap: ${wraps[wrap]};
    height: ${height};
    max-width: ${maxWidth};
    min-height: ${minHeight};
    overflow-x: ${scroll.includes("x") ? "auto" : "unset"};
    overflow-y: ${scroll.includes("y") ? "auto" : "unset"};
    position: ${position};
    transition: all 0.3s ease;
    ${getShadow(shadow, shadowBottom)}
    ${getBorder(
      borderColor,
      borderBottomColor,
      borderTopColor,
      leftBar,
      topBar
    )}

    @media screen and (min-width: 60em) {
      ${getWidth(width)}
      ${getJustify(justify)}
      ${getMinWidth(minWidth)}
    }

    @media screen and (min-width: 30em) and (max-width: 60em) {
      ${getWidth(width, widthMd)}
      ${getJustify(justify, justifyMd)}
      ${getMinWidth(minWidth, minWidthMd)}
      display: ${
        displayMd === undefined ? displays[display] : displays[displayMd]
      };
    }

    @media screen and (max-width: 30em) {
      ${getWidth(widthMd === undefined ? width : widthMd, widthSm)}
      ${getJustify(justifyMd === undefined ? justify : justifyMd, justifySm)}
      ${getMinWidth(
        minWidthMd === undefined ? minWidth : minWidthMd,
        minWidthSm
      )}
    display: ${
      displaySm === undefined ? displays[display] : displays[displaySm]
    };
    }

    :hover {
      ${getShadow(hoverShadow)}
      background: ${hovercolor};
      border: ${
        borderHoverColor === undefined ? "" : `1px solid ${borderHoverColor}`
      };
      color: ${textHoverColor};
    }
  `}
`;

export { StyledContainer };
