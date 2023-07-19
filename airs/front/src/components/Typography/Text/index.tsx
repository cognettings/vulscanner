import React from "react";

import { StyledText, StyledTextMarkdown } from "./styledComponents";
import type { ITextProps } from "./types";

const Text: React.FC<ITextProps> = ({
  children,
  color,
  display,
  fontStyle,
  hColor,
  mb,
  ml,
  mr,
  mt,
  size,
  sizeMd,
  sizeSm,
  textAlign,
  weight,
}): JSX.Element => {
  if (typeof children === "string") {
    return (
      <StyledTextMarkdown
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
        weight={weight}
      >
        {children}
      </StyledTextMarkdown>
    );
  }

  return (
    <StyledText
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
      weight={weight}
    >
      {children}
    </StyledText>
  );
};

export { Text };
