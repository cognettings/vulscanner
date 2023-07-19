import { useMatomo } from "@datapunt/matomo-tracker-react";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import { IoMdArrowDown } from "react-icons/io";
import { useWindowSize } from "usehooks-ts";

import {
  IconBlock,
  KnowLink,
  MainCoverHome,
  Span,
  Tag,
} from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Switch } from "../../../components/Switch";
import { Text, Title } from "../../../components/Typography";

const Header: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();
  const { trackEvent } = useMatomo();
  const [content, setContent] = useState(1);
  const plan: string = content === 1 ? "squad" : "machine";
  const { t } = useTranslation();
  const matomoFreeTrialEvent = useCallback((): void => {
    if (plan === "machine") {
      trackEvent({ action: "free-trial-click", category: "plans-header" });
    }
  }, [plan, trackEvent]);

  const title: JSX.Element[] = [
    <Text color={"#121216"} key={0} size={"medium"} weight={"semibold"}>
      {t("plansPage.header.machine.text")}
      &nbsp; &nbsp;
      <Tag>{t("plansPage.header.machine.tag")}</Tag>
    </Text>,
    <Text color={"#25252d"} key={1} size={"medium"} weight={"semibold"}>
      {t("plansPage.header.squad.keyword1")}
      <Span fColor={"#bf0b1a"}>{t("plansPage.header.squad.separator")}</Span>
      {t("plansPage.header.squad.keyword2")}
      <Span fColor={"#bf0b1a"}>{t("plansPage.header.squad.separator")}</Span>
      {t("plansPage.header.squad.keyword3")}
    </Text>,
  ];

  const tabs: string[] = ["Machine Plan", "Squad Plan"];

  return (
    <Container display={"flex"} height={"fit-content"} phSm={4} width={"100%"}>
      <MainCoverHome>
        <Container display={"flex"} justify={"center"} mb={5}>
          <Container
            display={"flex"}
            height={"fit-content"}
            justify={"center"}
            maxWidth={"1200px"}
            wrap={"wrap"}
          >
            <Title
              color={"#2e2e38"}
              level={3}
              mt={5}
              size={"big"}
              textAlign={"center"}
            >
              {t("plansPage.portrait.title")}
            </Title>
            <Container display={"flex"} justify={"center"} mt={4} wrap={"wrap"}>
              <Switch options={tabs} setState={setContent} state={content} />
            </Container>
          </Container>
        </Container>
        <Container
          display={"flex"}
          justify={"end"}
          width={"100%"}
          wrap={"wrap"}
        >
          <Container display={"flex"} maxWidth={"1600px"} wrap={"wrap"}>
            <Container
              display={"flex"}
              justify={"end"}
              pl={4}
              width={"60%"}
              widthMd={"100%"}
            >
              <Container>
                {title[content]}
                <Container maxWidth={"812px"} mt={3}>
                  <Title color={"#2e2e38"} level={3} mb={4} size={"medium"}>
                    {t(`plansPage.header.${plan}.title`)}
                  </Title>
                </Container>
                {[...Array(4).keys()].map(
                  (el: number): JSX.Element =>
                    el === 0 ? (
                      <div key={el} />
                    ) : (
                      <Container
                        display={"flex"}
                        key={el}
                        mb={4}
                        wrap={width < 960 ? "wrap" : "nowrap"}
                      >
                        <Container width={"fit-content"} widthSm={"100%"}>
                          <IconBlock key={`icon${el}`}>
                            <CloudImage
                              alt={"plans-icon"}
                              key={`icon-image${el}`}
                              src={`airs/plans/icon-${plan}-${el}.png`}
                            />
                          </IconBlock>
                        </Container>
                        <Container key={`container-${el}`}>
                          <Title
                            color={"#2e2e38"}
                            display={"block"}
                            key={`title${el}`}
                            level={3}
                            size={"xs"}
                          >
                            {t(`plansPage.header.${plan}.titleBenefit${el}`)}
                          </Title>
                          <Text
                            color={"#535365"}
                            display={"block"}
                            key={`text-${el}`}
                          >
                            {t(`plansPage.header.${plan}.textBenefit${el}`)}
                          </Text>
                        </Container>
                      </Container>
                    )
                )}
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"start"}
                  justifySm={"center"}
                  mb={4}
                  wrap={"wrap"}
                >
                  <AirsLink
                    href={
                      plan === "machine"
                        ? "https://app.fluidattacks.com/SignUp"
                        : "/contact-us/"
                    }
                  >
                    <Button
                      onClick={matomoFreeTrialEvent}
                      size={"md"}
                      variant={"primary"}
                    >
                      {plan === "machine"
                        ? t("plansPage.header.button.machine")
                        : t("plansPage.header.button.squad")}
                    </Button>
                  </AirsLink>
                  <KnowLink href={"#comparative-plans-table"}>
                    {t("plansPage.header.link")}
                    <IoMdArrowDown />
                  </KnowLink>
                </Container>
              </Container>
            </Container>
            <Container
              display={"flex"}
              justify={"end"}
              justifyMd={"center"}
              width={"40%"}
              widthMd={"100%"}
            >
              <CloudImage
                alt={"plans-header-image"}
                src={
                  width > 960
                    ? `airs/plans/header-${plan}.png`
                    : `airs/plans/header-${plan}-complete.png`
                }
                styles={"plans-header-img"}
              />
            </Container>
          </Container>
        </Container>
      </MainCoverHome>
    </Container>
  );
};

export { Header };
