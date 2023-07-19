import React from "react";
import { useTranslation } from "react-i18next";

import { PlansQuestion } from "./Question";

import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

const PlansFaq: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Container bgColor={"#f4f4f6"} width={"100%"}>
      <Container ph={2} pt={4} width={"98%"}>
        <Title
          color={"#2e2e38"}
          level={1}
          mb={3}
          size={"medium"}
          textAlign={"center"}
        >
          {t("plansPage.faqPlans.title")}
        </Title>
        <Text color={"#535365"} ml={2} mr={2} size={"big"} textAlign={"center"}>
          {t("plansPage.faqPlans.subtitle")}
        </Text>
      </Container>
      <Container center={true} maxWidth={"1200px"} pb={2} ph={4} pt={5}>
        <Title color={"#2e2e38"} level={3} mb={4} size={"smallBold"}>
          {t("plansPage.faqPlans.questions.about.title")}
        </Title>
        <PlansQuestion
          answer={t("plansPage.faqPlans.answers.about.1")}
          question={t("plansPage.faqPlans.questions.about.1")}
        />
      </Container>
      <Container center={true} maxWidth={"1200px"} pb={2} ph={4} pt={4}>
        <Title color={"#2e2e38"} level={3} mb={4} size={"smallBold"}>
          {t("plansPage.faqPlans.questions.benefits.title")}
        </Title>
        {[...Array(10).keys()].map(
          (el: number): JSX.Element =>
            el === 0 ? (
              <div key={`0`} />
            ) : (
              <PlansQuestion
                answer={t(`plansPage.faqPlans.answers.benefits.${el}`)}
                key={`question-${el}`}
                question={t(`plansPage.faqPlans.questions.benefits.${el}`)}
              />
            )
        )}
      </Container>
      <Container center={true} maxWidth={"1200px"} pb={2} ph={4} pt={4}>
        <Title color={"#2e2e38"} level={3} mb={4} size={"smallBold"}>
          {t("plansPage.faqPlans.questions.machine.title")}
        </Title>
        {[...Array(5).keys()].map(
          (el: number): JSX.Element =>
            el === 0 ? (
              <div key={`0`} />
            ) : (
              <PlansQuestion
                answer={t(`plansPage.faqPlans.answers.machine.${el}`)}
                key={`question-${el}`}
                question={t(`plansPage.faqPlans.questions.machine.${el}`)}
              />
            )
        )}
      </Container>
      <Container center={true} maxWidth={"1200px"} pb={5} ph={4} pt={4}>
        <Title color={"#2e2e38"} level={3} mb={4} size={"smallBold"}>
          {t("plansPage.faqPlans.questions.informationSecurity.title")}
        </Title>
        <PlansQuestion
          answer={t("plansPage.faqPlans.answers.informationSecurity.1")}
          question={t("plansPage.faqPlans.questions.informationSecurity.1")}
        />
      </Container>
    </Container>
  );
};

export { PlansFaq };
