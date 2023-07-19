import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { PlanTag, PlansGrid, Tag } from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

const ContinuousHackingPlans: React.FC = (): JSX.Element => {
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
      pt={5}
      wrap={"wrap"}
    >
      <Container bgColor={"#ffffff"} maxWidth={"1210px"}>
        <Title
          color={"#2e2e38"}
          level={2}
          mb={4}
          size={"big"}
          textAlign={"center"}
        >
          {t("continuousHackingPage.plans.title")}
        </Title>
      </Container>
      <PlansGrid>
        <PlanTag>
          <Container align={"end"} display={"flex"} justify={"center"}>
            <Title color={"#2e2e38"} level={2} ml={3} mt={4} size={"medium"}>
              {t("continuousHackingPage.plans.machine.title")}
            </Title>
            <Container pb={2} width={"100%"}>
              <Tag>{t("plansPage.header.machine.tag")}</Tag>
            </Container>
          </Container>
          <Text color={"#1D2939"} ml={3} mt={4} size={"big"}>
            {t("continuousHackingPage.plans.machine.subtitle")}
          </Text>
          <Container
            display={"flex"}
            justify={"start"}
            justifyMd={"center"}
            justifySm={"unset"}
            mv={4}
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
        </PlanTag>
        <PlanTag>
          <Container align={"end"} display={"flex"} justify={"center"}>
            <Title color={"#2e2e38"} level={2} ml={3} mt={4} size={"medium"}>
              {t("continuousHackingPage.plans.squad.title")}
            </Title>
          </Container>
          <Container width={"80%"}>
            <Text color={"#1D2939"} ml={3} mt={4} size={"big"}>
              {t("continuousHackingPage.plans.squad.subtitle")}
            </Text>
          </Container>

          <Container
            display={"flex"}
            justify={"start"}
            justifyMd={"center"}
            justifySm={"unset"}
            mv={4}
            wrap={"wrap"}
          >
            <Container ph={3} phSm={0} pv={1} width={"auto"} widthSm={"100%"}>
              <AirsLink decoration={"none"} href={"/plans/"}>
                <Button display={"block"} variant={"tertiary"}>
                  {t("continuousHackingPage.plans.squad.button")}
                </Button>
              </AirsLink>
            </Container>
          </Container>
        </PlanTag>
      </PlansGrid>
    </Container>
  );
};

export { ContinuousHackingPlans };
