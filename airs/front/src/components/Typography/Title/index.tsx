import React from "react";

import { StyledTitle, StyledTitleMarkdown } from "./styledComponents";
import type { ITitleProps } from "./types";

const Title: React.FC<ITitleProps> = ({
  children,
  color,
  display,
  fontStyle,
  hColor,
  level,
  mb,
  ml,
  mr,
  mt,
  size,
  sizeMd,
  sizeSm,
  textAlign,
}): JSX.Element => {
  if (typeof children === "string") {
    return (
      <StyledTitleMarkdown
        as={`h${level}`}
        color={color}
        display={display}
        fontStyle={fontStyle}
        hColor={hColor}
        mb={mb}
        ml={ml}
        mr={mr}
        mt={mt}
        size={size}
        sizeMd={sizeMd}
        sizeSm={sizeSm}
        textAlign={textAlign}
      >
        {children}
      </StyledTitleMarkdown>
    );
  }

  return (
    <StyledTitle
      as={`h${level}`}
      color={color}
      display={display}
      fontStyle={fontStyle}
      hColor={hColor}
      mb={mb}
      ml={ml}
      mr={mr}
      mt={mt}
      size={size}
      sizeMd={sizeMd}
      sizeSm={sizeSm}
      textAlign={textAlign}
    >
      {children}
    </StyledTitle>
  );
};

export { Title };
