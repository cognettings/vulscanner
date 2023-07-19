import React from "react";
import { useTranslation } from "react-i18next";
import { useWindowSize } from "usehooks-ts";

import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { Hero } from "../../../components/Hero";
import { SimpleCard } from "../../../components/SimpleCard";
import { Text, Title } from "../../../components/Typography";

const ContinuousHackingHeader: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();
  const { t } = useTranslation();

  return (
    <Container bgGradient={"110.83deg, #2E2E38 1.35%, #121216 99.1%"}>
      <Hero
        button1Link={"https://app.fluidattacks.com/SignUp"}
        button1Text={t("continuousHackingPage.portrait.hero.button1")}
        button2Link={"/contact-us/"}
        button2Text={t("continuousHackingPage.portrait.hero.button2")}
        image={"airs/services/continuous-hacking/header-hero.png"}
        matomoAction={"ContinuousHacking"}
        paragraph={t("continuousHackingPage.portrait.hero.paragraph")}
        subtitle={t("continuousHackingPage.portrait.hero.subtitle")}
        title={t("continuousHackingPage.portrait.hero.title")}
        tone={"darkGradient"}
        variant={"center"}
      />
      <Title
        color={"#ffffff"}
        level={1}
        ml={2}
        mr={2}
        mt={3}
        size={width < 480 ? "small" : "medium"}
        textAlign={"center"}
      >
        {t("continuousHackingPage.portrait.title")}
      </Title>
      <Text color={"#ffffff"} size={"big"} textAlign={"center"}>
        {t("continuousHackingPage.portrait.subtitle")}
      </Text>
      <Container
        center={true}
        maxWidth={width > 960 ? "1550px" : "760px"}
        mt={4}
        pb={5}
        ph={4}
      >
        <Grid columns={4} columnsMd={2} columnsSm={1} gap={"1rem"}>
          <SimpleCard
            bgGradient={"180deg, #3A3A46 0%, #121216 100%"}
            br={4}
            description={t("continuousHackingPage.portrait.card1.subtitle")}
            descriptionColor={"#ffffff"}
            image={"airs/services/continuous-hacking/card1.png"}
            maxWidth={"310px"}
            title={t("continuousHackingPage.portrait.card1.title")}
            titleColor={"#ffffff"}
            titleSize={"xs"}
          />
          <SimpleCard
            bgGradient={"180deg, #3A3A46 0%, #121216 100%"}
            br={4}
            description={t("continuousHackingPage.portrait.card2.subtitle")}
            descriptionColor={"#ffffff"}
            image={"airs/services/continuous-hacking/card2.png"}
            maxWidth={"310px"}
            title={t("continuousHackingPage.portrait.card2.title")}
            titleColor={"#ffffff"}
            titleSize={"xs"}
          />
          <SimpleCard
            bgGradient={"180deg, #3A3A46 0%, #121216 100%"}
            br={4}
            description={t("continuousHackingPage.portrait.card3.subtitle")}
            descriptionColor={"#ffffff"}
            image={"airs/services/continuous-hacking/card3.png"}
            maxWidth={"310px"}
            title={t("continuousHackingPage.portrait.card3.title")}
            titleColor={"#ffffff"}
            titleSize={"xs"}
          />
          <SimpleCard
            bgGradient={"180deg, #3A3A46 0%, #121216 100%"}
            br={4}
            description={t("continuousHackingPage.portrait.card4.subtitle")}
            descriptionColor={"#ffffff"}
            image={"airs/services/continuous-hacking/card4.png"}
            maxWidth={"310px"}
            title={t("continuousHackingPage.portrait.card4.title")}
            titleColor={"#ffffff"}
            titleSize={"xs"}
          />
        </Grid>
      </Container>
    </Container>
  );
};

export { ContinuousHackingHeader };
