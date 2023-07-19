import React from "react";
import { BsArrowRightShort } from "react-icons/bs";

import { CardFooter, CardLink } from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";
import { i18next, translate } from "../../../utils/translations/translate";

const Reviews: React.FC = (): JSX.Element => {
  const lng = i18next.language;
  const landingLng = lng === "en" ? "case-study" : "es/caso-exito";

  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
      display={"flex"}
      justify={"center"}
      minHeight={"500px"}
      wrap={"wrap"}
    >
      <Container maxWidth={"700px"} minWidth={"300px"} mt={5} ph={4} phMd={4}>
        <Title color={"#2e2e38"} level={1} mb={1} size={"medium"}>
          {translate.t("home.reviews.title")}
        </Title>
        <Text color={"#535365"} mb={4} mt={4} size={"big"}>
          {translate.t("home.reviews.subtitle")}
        </Text>
        <Container display={"flex"} wrap={"wrap"}>
          <AirsLink
            decoration={"underline"}
            hovercolor={"#bf0b1a"}
            href={"https://clutch.co/profile/fluid-attacks"}
          >
            <Text color={"#2e2e38"} mr={1} mt={3} size={"big"} weight={"bold"}>
              {translate.t("home.reviews.public")}
            </Text>
          </AirsLink>
          <CloudImage
            alt={"reviews image"}
            src={"airs/home/SuccessReviews/reviews.png"}
            styles={"mv2 mh2 w4"}
          />
        </Container>
      </Container>
      <Container
        align={"center"}
        display={"flex"}
        justify={"center"}
        maxWidth={"750px"}
        wrap={"wrap"}
      >
        <Container
          align={"start"}
          bgGradient={"#ffffff, #f4f4f6"}
          borderColor={"#dddde3"}
          br={2}
          direction={"column"}
          display={"flex"}
          height={"357px"}
          hoverShadow={true}
          hovercolor={"#ffffff"}
          mh={3}
          mv={3}
          width={"338px"}
        >
          <CardLink>
            <Title color={"#bf0b1a"} level={4} size={"xxs"}>
              {translate.t("home.reviews.successStory.title")}
            </Title>
            <CloudImage
              alt={"success story 1"}
              src={"airs/home/SuccessReviews/logo-payvalida.png"}
              styles={"mv3 w-50"}
            />
            <Text color={"#535365"} mb={2} size={"medium"}>
              {translate.t("home.reviews.successStory.description1")}
            </Text>
            <CardFooter id={"link"}>
              <Container align={"center"} display={"flex"} pv={4} wrap={"wrap"}>
                <AirsLink
                  decoration={"underline"}
                  href={`https://try.fluidattacks.tech/${landingLng}/payvalida/`}
                >
                  <Text color={"#2e2e38"} mr={1} size={"small"} weight={"bold"}>
                    {translate.t("home.reviews.link")}
                  </Text>
                </AirsLink>
                <BsArrowRightShort size={20} />
              </Container>
            </CardFooter>
          </CardLink>
        </Container>
        <Container
          align={"start"}
          bgGradient={"#ffffff, #f4f4f6"}
          borderColor={"#dddde3"}
          br={2}
          direction={"column"}
          display={"flex"}
          height={"357px"}
          hoverShadow={true}
          hovercolor={"#ffffff"}
          width={"338px"}
        >
          <CardLink>
            <Title color={"#bf0b1a"} level={4} size={"xxs"}>
              {translate.t("home.reviews.successStory.title")}
            </Title>
            <CloudImage
              alt={"success story 2"}
              src={"airs/home/SuccessReviews/logo_proteccion.png"}
              styles={"mv3 w-50"}
            />
            <Text color={"#535365"} size={"medium"}>
              {translate.t("home.reviews.successStory.description2")}
            </Text>
            <CardFooter id={"link"}>
              <Container align={"center"} display={"flex"} pv={4} wrap={"wrap"}>
                <AirsLink
                  decoration={"underline"}
                  href={`https://try.fluidattacks.tech/${landingLng}/proteccion/`}
                >
                  <Text color={"#2e2e38"} mr={1} size={"small"} weight={"bold"}>
                    {translate.t("home.reviews.link")}
                  </Text>
                </AirsLink>
                <BsArrowRightShort size={20} />
              </Container>
            </CardFooter>
          </CardLink>
        </Container>
      </Container>
    </Container>
  );
};

export { Reviews };
