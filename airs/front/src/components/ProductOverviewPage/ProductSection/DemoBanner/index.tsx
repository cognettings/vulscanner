import React from "react";

import {
  BannerContainer,
  CardContainer,
  ImageContainer,
  TextContainer,
} from "./styledComponents";

import { Text, Title } from "../../../Typography";
import { InteractiveImage } from "../InteractiveImage";

interface IDemoProps {
  description: string;
  hasHotSpot: boolean;
  image1: string;
  image2: string;
  imageRight: boolean;
  subtitle: string;
  title: string;
}

const DemoBanner: React.FC<IDemoProps> = ({
  description,
  hasHotSpot,
  image1,
  image2,
  imageRight,
  subtitle,
  title,
}: IDemoProps): JSX.Element => {
  return (
    <React.Fragment>
      {imageRight ? (
        <BannerContainer>
          <TextContainer>
            <Title color={"#bf0b1a"} level={3} size={"xs"}>
              {title}
            </Title>
            <Title color={"#2e2e38"} level={3} mt={3} size={"small"}>
              {subtitle}
            </Title>
            <Text color={"#5c5c70"} mt={3} size={"medium"}>
              {description}
            </Text>
          </TextContainer>
          <ImageContainer margin={imageRight}>
            <InteractiveImage
              hasHotSpot={hasHotSpot}
              image1={`/airs/product-overview/color/${image1}`}
              image2={`/airs/product-overview/color/${image2}`}
              isRight={imageRight}
            />
          </ImageContainer>
        </BannerContainer>
      ) : (
        <BannerContainer>
          <ImageContainer margin={imageRight}>
            <InteractiveImage
              hasHotSpot={hasHotSpot}
              image1={`/airs/product-overview/color/${image1}`}
              image2={`/airs/product-overview/color/${image2}`}
              isRight={imageRight}
            />
          </ImageContainer>
          <TextContainer>
            <Title color={"#bf0b1a"} level={3} size={"xs"}>
              {title}
            </Title>
            <Title color={"#2e2e38"} level={3} mt={3} size={"small"}>
              {subtitle}
            </Title>
            <Text color={"#5c5c70"} mt={3} size={"medium"}>
              {description}
            </Text>
          </TextContainer>
        </BannerContainer>
      )}
      <CardContainer>
        <TextContainer>
          <Title color={"#bf0b1a"} level={3} size={"xs"}>
            {title}
          </Title>
          <Title color={"#2e2e38"} level={3} mt={3} size={"small"}>
            {subtitle}
          </Title>
          <Text color={"#5c5c70"} mt={3} size={"medium"}>
            {description}
          </Text>
        </TextContainer>
        <ImageContainer margin={false}>
          <InteractiveImage
            hasHotSpot={hasHotSpot}
            image1={`/airs/product-overview/color/${image1}`}
            image2={`/airs/product-overview/color/${image2}`}
            isRight={false}
          />
        </ImageContainer>
      </CardContainer>
    </React.Fragment>
  );
};

export { DemoBanner };
