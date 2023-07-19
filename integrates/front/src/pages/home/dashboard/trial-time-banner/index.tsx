import { faArrowRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";

import { ArrowContainer } from "./styles";

import { Container } from "components/Container";
import { ExternalLinkOutline } from "components/ExternalLink";
import { Text } from "components/Text";
import { useTrial } from "hooks/use-trial";

const TrialTimeBanner: React.FC = (): JSX.Element | null => {
  const trialData = useTrial();

  if (trialData === null) {
    return null;
  }

  const { trial, remainingDays } = trialData;

  if (trial.completed) {
    return null;
  }

  return (
    <Container
      align={"center"}
      bgColor={"#2e2e38"}
      display={"flex"}
      justify={"center"}
      minHeight={"44px"}
      pb={"8px"}
      pt={"8px"}
      scroll={"none"}
    >
      <Text disp={"inline"} fw={7} tone={"light"}>
        {`You have ${remainingDays} days of free trial left`}
      </Text>
      <ArrowContainer>
        <Text disp={"inline"} fw={7} tone={"light"}>
          <ExternalLinkOutline
            href={
              "https://res.cloudinary.com/fluid-attacks/image/upload/fl_attachment:Fluid-Attacks-Plans/v1678888081/integrates/plans/fluid-attacks-plans.pdf"
            }
          >
            {"Learn about our plans"}
          </ExternalLinkOutline>
          <FontAwesomeIcon icon={faArrowRight} />
        </Text>
      </ArrowContainer>
    </Container>
  );
};

export { TrialTimeBanner };
