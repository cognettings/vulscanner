import React, { useLayoutEffect } from "react";
import { useTranslation } from "react-i18next";
import { useWindowSize } from "usehooks-ts";

import { ContentCard } from "./ContentCard";
import { DiscoverOnMobile } from "./MobileContent";
import { ContentColumn, ContinuousRow, VectorColumn } from "./styledComponents";
import { Vector } from "./Vector";

import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Title } from "../../../components/Typography";

const DiscoverContinuousHacking: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();
  const { t } = useTranslation();
  const cards = [
    {
      icon: "airs/services/continuous-hacking/discover/icon1.png",
      paragraph: t("continuousHackingPage.discover.content.card1.paragraph"),
      subtitle: t("continuousHackingPage.discover.content.card1.subtitle"),
      title: t("continuousHackingPage.discover.content.card1.title"),
    },
    {
      icon: "airs/services/continuous-hacking/discover/icon2.png",
      paragraph: t("continuousHackingPage.discover.content.card2.paragraph"),
      subtitle: t("continuousHackingPage.discover.content.card2.subtitle"),
      title: t("continuousHackingPage.discover.content.card2.title"),
    },
    {
      icon: "airs/services/continuous-hacking/discover/icon3.png",
      paragraph: t("continuousHackingPage.discover.content.card3.paragraph"),
      subtitle: t("continuousHackingPage.discover.content.card3.subtitle"),
      title: t("continuousHackingPage.discover.content.card3.title"),
    },
    {
      icon: "airs/services/continuous-hacking/discover/icon4.png",
      paragraph: t("continuousHackingPage.discover.content.card4.paragraph"),
      subtitle: t("continuousHackingPage.discover.content.card4.subtitle"),
      title: t("continuousHackingPage.discover.content.card4.title"),
    },
  ];

  useLayoutEffect((): (() => void) => {
    const onScroll = (): void => {
      const scrollDistance = -document
        .getElementsByClassName("discover-section")[0]
        .getBoundingClientRect().top;
      const progressPercentage =
        document.getElementsByClassName("discover-section")[0].scrollHeight -
        document.documentElement.clientHeight;
      const scrolled = scrollDistance / progressPercentage;
      const path = document.getElementById("vector") as SVGPathElement | null;
      if (!path) {
        return;
      }
      const pathLength = path.getTotalLength();
      const pointOnPath = path.getPointAtLength(pathLength * (scrolled - 0.05));
      const dot = document.getElementById("dot") as SVGElement | null;
      dot?.setAttribute(
        "transform",
        `translate(${pointOnPath.x},${pointOnPath.y})`
      );
    };
    window.addEventListener("scroll", onScroll);

    return (): void => {
      window.removeEventListener("scroll", onScroll);
    };
  }, []);
  if (width < 1140) {
    return <DiscoverOnMobile />;
  }

  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
      classname={"discover-section"}
      display={"flex"}
      justify={"center"}
      wrap={"wrap"}
    >
      <Container maxWidth={"1210px"} mh={4}>
        <Title
          color={"#bf0b1a"}
          level={2}
          mb={4}
          mt={5}
          size={"small"}
          textAlign={"center"}
        >
          {t("continuousHackingPage.discover.subtitle")}
        </Title>
        <Title color={"#2e2e38"} level={2} size={"big"} textAlign={"center"}>
          {t("continuousHackingPage.discover.title")}
        </Title>
      </Container>
      <ContinuousRow>
        <ContentColumn>
          <ContentCard
            icon={cards[0].icon}
            mb={7}
            mt={6}
            paragraph={cards[0].paragraph}
            subtitle={cards[0].subtitle}
            title={cards[0].title}
          />
          <CloudImage
            alt={"discoverImage1"}
            src={"airs/services/continuous-hacking/discover/image2.png"}
            styles={"mb5"}
          />
          <ContentCard
            icon={cards[2].icon}
            mb={5}
            mt={6}
            paragraph={cards[2].paragraph}
            subtitle={cards[2].subtitle}
            title={cards[2].title}
          />
          <CloudImage
            alt={"discoverImage1"}
            src={"airs/services/continuous-hacking/discover/image4.png"}
            styles={"mt5"}
          />
        </ContentColumn>
        <VectorColumn>
          <Vector />
        </VectorColumn>
        <ContentColumn>
          <CloudImage
            alt={"discoverImage1"}
            src={"airs/services/continuous-hacking/discover/image1.png"}
          />
          <ContentCard
            icon={cards[1].icon}
            mb={7}
            mt={7}
            paragraph={cards[1].paragraph}
            subtitle={cards[1].subtitle}
            title={cards[1].title}
          />
          <CloudImage
            alt={"discoverImage1"}
            src={"airs/services/continuous-hacking/discover/image3.png"}
          />
          <ContentCard
            icon={cards[3].icon}
            mb={1}
            mt={6}
            paragraph={cards[3].paragraph}
            subtitle={cards[3].subtitle}
            title={cards[3].title}
          />
        </ContentColumn>
      </ContinuousRow>
    </Container>
  );
};

export { DiscoverContinuousHacking };
