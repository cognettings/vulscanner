import React from "react";
import { useTranslation } from "react-i18next";

import { ContentCard } from "./ContentCard";
import { ContinuousRow } from "./styledComponents";

import { Container } from "../../../components/Container";
import { Title } from "../../../components/Typography";

const DiscoverOnMobile: React.FC = (): JSX.Element => {
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

  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
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
        <ContentCard
          icon={cards[0].icon}
          mb={2}
          mt={5}
          paragraph={cards[0].paragraph}
          subtitle={cards[0].subtitle}
          title={cards[0].title}
        />
        <ContentCard
          icon={cards[2].icon}
          mb={2}
          mt={5}
          paragraph={cards[2].paragraph}
          subtitle={cards[2].subtitle}
          title={cards[2].title}
        />
        <ContentCard
          icon={cards[1].icon}
          mb={2}
          mt={5}
          paragraph={cards[1].paragraph}
          subtitle={cards[1].subtitle}
          title={cards[1].title}
        />
        <ContentCard
          icon={cards[3].icon}
          mb={2}
          mt={5}
          paragraph={cards[3].paragraph}
          subtitle={cards[3].subtitle}
          title={cards[3].title}
        />
      </ContinuousRow>
    </Container>
  );
};

export { DiscoverOnMobile };
