/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import i18next from "i18next";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { BsArrowRightShort } from "react-icons/bs";

import {
  CardFooter,
  CardLink,
  MainCoverHome,
  SlideShow,
  SolutionsContainer,
} from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";
import { useWindowSize } from "../../../utils/hooks/useWindowSize";
import { translatedPages } from "../../../utils/translations/spanishPages";

const SolutionsSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { width } = useWindowSize();

  const data = [
    {
      description: t("solutions.homeCards.devSecOps.paragraph"),
      title: t("solutions.homeCards.devSecOps.title"),
      urlCard: "/solutions/devsecops/",
    },
    {
      description: t("solutions.homeCards.secureCode.paragraph"),
      title: t("solutions.homeCards.secureCode.title"),
      urlCard: "/solutions/secure-code-review/",
    },
    {
      description: t("solutions.homeCards.redTeaming.paragraph"),
      title: t("solutions.homeCards.redTeaming.title"),
      urlCard: "/solutions/red-teaming/",
    },
    {
      description: t("solutions.homeCards.securityTesting.paragraph"),
      title: t("solutions.homeCards.securityTesting.title"),
      urlCard: "/solutions/security-testing/",
    },
    {
      description: t("solutions.homeCards.penetrationTesting.paragraph"),
      title: t("solutions.homeCards.penetrationTesting.title"),
      urlCard: "/solutions/penetration-testing/",
    },
    {
      description: t("solutions.homeCards.ethicalHacking.paragraph"),
      title: t("solutions.homeCards.ethicalHacking.title"),
      urlCard: "/solutions/ethical-hacking/",
    },
    {
      description: t("solutions.homeCards.vulnerabilityManagement.paragraph"),
      title: t("solutions.homeCards.vulnerabilityManagement.title"),
      urlCard: "/solutions/vulnerability-management/",
    },
  ];

  const handleClick = useCallback(
    (url: string): (() => void) =>
      (): void => {
        const currentLanguage = i18next.language;
        const spanishUrl: { en: string; es: string } | undefined =
          translatedPages.find((page): boolean => page.en === url);
        const locationEs = spanishUrl
          ? spanishUrl.es
            ? spanishUrl.es
            : url
          : url;
        const translatedLocation =
          currentLanguage === "es" ? locationEs.replace("/es", "") : url;
        if (typeof window !== "undefined") {
          const actLocation: string = window.location.href;
          window.location.assign(
            actLocation.concat(translatedLocation.slice(1))
          );
        }
      },
    []
  );

  return (
    <MainCoverHome>
      <Container>
        <Container
          align={"center"}
          center={true}
          display={"flex"}
          justify={"center"}
          maxWidth={"850px"}
          mb={4}
          minHeight={"360px"}
          wrap={"wrap"}
        >
          <Title
            color={"#ffffff"}
            level={1}
            mb={4}
            ml={2}
            mr={2}
            mt={5}
            size={"medium"}
            textAlign={"center"}
          >
            {t("home.solutions.title")}
          </Title>
          <Text color={"#b0b0bf"} mb={4} size={"big"} textAlign={"center"}>
            {t("home.solutions.subtitle")}
          </Text>
          <AirsLink href={"/solutions/"}>
            <Button display={"block"} variant={"primary"}>
              {t("home.solutions.button")}
            </Button>
          </AirsLink>
        </Container>
        <SolutionsContainer gradientColor={"#fffff"} maxWidth={width}>
          <SlideShow>
            {[...Array(2).keys()].map((): JSX.Element[] =>
              data.map(
                (card): JSX.Element => (
                  <Container
                    align={"start"}
                    bgGradient={"#ffffff, #f4f4f6"}
                    borderColor={"#dddde3"}
                    borderHoverColor={"#bf0b1a"}
                    br={2}
                    direction={"column"}
                    display={"flex"}
                    height={"318px"}
                    hovercolor={"#ffe5e7"}
                    key={card.urlCard}
                    onClick={handleClick(card.urlCard)}
                    ph={3}
                    pv={3}
                    width={"338px"}
                  >
                    <CardLink>
                      <Title color={"#bf0b1a"} level={4} size={"xxs"}>
                        {t("home.solutions.cardTitle")}
                      </Title>
                      <Title
                        color={"#2e2e38"}
                        level={4}
                        mb={3}
                        mt={3}
                        size={"small"}
                      >
                        {card.title}
                      </Title>
                      <Text color={"#535365"} size={"medium"}>
                        {card.description}
                      </Text>
                      <CardFooter id={"link"}>
                        <Container
                          align={"center"}
                          display={"flex"}
                          pb={2}
                          pt={4}
                          wrap={"wrap"}
                        >
                          <AirsLink
                            decoration={"underline"}
                            href={card.urlCard}
                          >
                            <Text
                              color={"#2e2e38"}
                              size={"small"}
                              weight={"bold"}
                            >
                              {t("home.solutions.cardLink")}
                            </Text>
                          </AirsLink>
                          <BsArrowRightShort size={20} />
                        </Container>
                      </CardFooter>
                    </CardLink>
                  </Container>
                )
              )
            )}
          </SlideShow>
        </SolutionsContainer>
      </Container>
    </MainCoverHome>
  );
};

export { SolutionsSection };
