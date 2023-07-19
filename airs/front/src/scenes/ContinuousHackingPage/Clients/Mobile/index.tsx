import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useWindowSize } from "usehooks-ts";

import { AirsLink } from "../../../../components/AirsLink";
import { Button } from "../../../../components/Button";
import { CloudImage } from "../../../../components/CloudImage";
import { Container } from "../../../../components/Container";
import { Text, Title } from "../../../../components/Typography";
import { Card } from "../styledComponents";

const ContinuousHackingClientsMobile: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();
  const { trackEvent } = useMatomo();
  const { t } = useTranslation();
  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "plans-click",
      category: "continuous-hacking",
    });
  }, [trackEvent]);

  return (
    <Container
      align={"center"}
      bgColor={"#ffffff"}
      display={"flex"}
      justify={"center"}
      pb={6}
      pt={6}
      wrap={"wrap"}
    >
      <Container
        display={"flex"}
        justify={"center"}
        maxWidth={"1280px"}
        width={"100%"}
        wrap={"wrap"}
      >
        <Container
          align={"center"}
          display={"flex"}
          justify={"center"}
          width={"100%"}
        >
          <Container maxWidth={"1210px"} ml={3}>
            <Title
              color={"#bf0b1a"}
              level={2}
              mb={2}
              mt={5}
              size={"small"}
              textAlign={"center"}
            >
              {t("continuousHackingPage.clients.subtitle")}
            </Title>
            <Title
              color={"#2e2e38"}
              level={2}
              mb={4}
              size={"medium"}
              textAlign={"center"}
            >
              {t("continuousHackingPage.clients.title")}
            </Title>
            <Container
              align={"center"}
              display={"flex"}
              justify={"center"}
              mb={2}
            >
              <Text color={"#25252d"} ml={5} mr={5} textAlign={"center"}>
                {t("continuousHackingPage.clients.paragraph")}
              </Text>
            </Container>
            <Container
              display={"flex"}
              justify={"start"}
              justifyMd={"center"}
              justifySm={"unset"}
              mv={5}
              wrap={"wrap"}
            >
              <Container pv={1} width={"auto"} widthSm={"100%"}>
                <AirsLink
                  decoration={"none"}
                  href={"https://app.fluidattacks.com/SignUp"}
                >
                  <Button
                    display={"block"}
                    onClick={matomoFreeTrialEvent}
                    variant={"primary"}
                  >
                    {t("continuousHackingPage.plans.machine.button1")}
                  </Button>
                </AirsLink>
              </Container>
              <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
                <AirsLink decoration={"none"} href={"/plans/"}>
                  <Button display={"block"} variant={"tertiary"}>
                    {t("continuousHackingPage.plans.machine.button2")}
                  </Button>
                </AirsLink>
              </Container>
            </Container>
          </Container>
        </Container>
        <Container
          display={"flex"}
          justify={width > 480 ? "end" : "center"}
          maxWidth={"680px"}
          width={"100%"}
          wrap={"wrap"}
        >
          <Card>
            <Container height={"48px"} mb={3} width={"48px"}>
              <CloudImage
                alt={"continuous-hacking-clients-icon1"}
                src={"airs/services/continuous-hacking/clients/icon1.png"}
                styles={"w-100"}
              />
            </Container>
            <Container>
              <Title color={"#ffffff"} level={3} size={"xxs"}>
                {t("continuousHackingPage.clients.card1.title")}
              </Title>
            </Container>
            <Container>
              <Title color={"#ffffff"} level={2} size={"medium"}>
                {t("continuousHackingPage.clients.card1.percentage")}
              </Title>
            </Container>
          </Card>
          <Card>
            <Container height={"48px"} mb={3} width={"48px"}>
              <CloudImage
                alt={"continuous-hacking-clients-icon2"}
                src={"airs/services/continuous-hacking/clients/icon2.png"}
                styles={"w-100"}
              />
            </Container>
            <Container>
              <Title color={"#ffffff"} level={3} size={"xxs"}>
                {t("continuousHackingPage.clients.card2.title")}
              </Title>
            </Container>
            <Container>
              <Title color={"#ffffff"} level={2} size={"medium"}>
                {t("continuousHackingPage.clients.card2.percentage")}
              </Title>
            </Container>
          </Card>
          <Card>
            <Container height={"48px"} mb={3} width={"48px"}>
              <CloudImage
                alt={"continuous-hacking-clients-icon3"}
                src={"airs/services/continuous-hacking/clients/icon3.png"}
                styles={"w-100"}
              />
            </Container>
            <Container>
              <Title color={"#ffffff"} level={3} size={"xxs"}>
                {t("continuousHackingPage.clients.card3.title")}
              </Title>
            </Container>
            <Container>
              <Title color={"#ffffff"} level={2} size={"medium"}>
                {t("continuousHackingPage.clients.card3.percentage")}
              </Title>
            </Container>
          </Card>
          <Card>
            <Container height={"48px"} mb={3} width={"48px"}>
              <CloudImage
                alt={"continuous-hacking-clients-icon4"}
                src={"airs/services/continuous-hacking/clients/icon4.png"}
                styles={"w-100"}
              />
            </Container>
            <Container>
              <Title color={"#ffffff"} level={3} size={"xxs"}>
                {t("continuousHackingPage.clients.card4.title")}
              </Title>
            </Container>
            <Container>
              <Title color={"#ffffff"} level={2} size={"medium"}>
                {t("continuousHackingPage.clients.card4.percentage")}
              </Title>
            </Container>
          </Card>
        </Container>
      </Container>
    </Container>
  );
};

export { ContinuousHackingClientsMobile };
