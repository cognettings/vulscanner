import React from "react";
import { ReactMarkdown } from "react-markdown/lib/react-markdown";

import type { ISimpleCardProps } from "./types";

import { CloudImage } from "../CloudImage";
import { Container } from "../Container";
import { Text, Title } from "../Typography";

const SimpleCard: React.FC<ISimpleCardProps> = ({
  bgColor,
  bgGradient,
  borderColor,
  br,
  description,
  descriptionColor,
  hovercolor,
  hoverShadow,
  image,
  title = "",
  titleColor = "unset",
  titleMinHeight,
  titleSize = "small",
  maxWidth,
  widthMd,
  widthSm,
}): JSX.Element => {
  if (title) {
    return (
      <Container
        bgColor={bgColor}
        bgGradient={bgGradient}
        borderColor={borderColor}
        br={br === undefined ? 2 : br}
        direction={"column"}
        display={"flex"}
        hoverShadow={hoverShadow}
        hovercolor={hovercolor}
        maxWidth={maxWidth}
        mh={2}
        mv={2}
        ph={3}
        pv={3}
        widthMd={widthMd}
        widthSm={widthSm}
      >
        <Container height={"48px"} mv={3} width={"48px"}>
          <CloudImage alt={title} src={image} styles={"w-100 h-100"} />
        </Container>
        <Container minHeight={titleMinHeight}>
          <Title color={titleColor} level={3} size={titleSize}>
            {title}
          </Title>
        </Container>
        <Container mv={3}>
          <Text color={descriptionColor} size={"small"}>
            {description}
          </Text>
        </Container>
      </Container>
    );
  }

  return (
    <Container
      bgColor={bgColor}
      bgGradient={bgGradient}
      borderColor={borderColor}
      br={br === undefined ? 2 : br}
      direction={"column"}
      display={"flex"}
      hoverShadow={hoverShadow}
      hovercolor={hovercolor}
      maxWidth={maxWidth}
      mh={2}
      mv={2}
      ph={3}
      pv={3}
      widthMd={widthMd}
      widthSm={widthSm}
    >
      <Container center={true} height={"64px"} mv={3} width={"64px"}>
        <CloudImage alt={image} src={image} styles={"w-100 h-100"} />
      </Container>
      <Container mb={3}>
        <Text color={descriptionColor} size={"small"} textAlign={"center"}>
          <ReactMarkdown>{description}</ReactMarkdown>
        </Text>
      </Container>
    </Container>
  );
};

export { SimpleCard };
