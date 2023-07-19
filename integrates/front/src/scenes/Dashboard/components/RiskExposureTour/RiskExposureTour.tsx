import { faClose } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback } from "react";
import { useHistory, useRouteMatch } from "react-router-dom";

import type { IRiskExposureTourProps } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Text } from "components/Text";
import { BaseStep, Tour } from "components/Tour";
import { useTour } from "hooks";

const RiskExposureTour: React.FC<IRiskExposureTourProps> = ({
  findingId,
  findingRiskExposure,
  step,
}): JSX.Element => {
  const { push } = useHistory();
  const { url } = useRouteMatch();

  const tourStyle = {
    options: {
      arrowColor: "#2e2e38",
      backgroundColor: "#2e2e38",
      overlayColor: "transparent",
      primaryColor: "#000",
      textColor: "#fff",
      width: 450,
    },
  };

  const { tours, setCompleted } = useTour();
  const runRiskExposureTour = !tours.newRiskExposure;

  const finishTour = useCallback((): void => {
    setCompleted("newRiskExposure");
  }, [setCompleted]);

  const goToFirstFinding = useCallback((): void => {
    push(`${url}/${findingId ?? ""}/locations`);
  }, [findingId, push, url]);

  if (runRiskExposureTour && step === 1) {
    return (
      <Tour
        onFinish={finishTour}
        run={runRiskExposureTour}
        steps={[
          {
            ...BaseStep,
            content: (
              <Container>
                <Container align={"center"} display={"flex"} justify={"end"}>
                  <Button
                    icon={faClose}
                    id={"close-tour"}
                    onClick={finishTour}
                    variant={"secondary"}
                  />
                </Container>
                <Container pt={"10px"}>
                  <Text
                    fw={7}
                    mb={2}
                    tone={"light"}
                  >{`New feature: ${findingRiskExposure} Risk exposure.`}</Text>
                  <Text tone={"light"}>
                    <span className={"fw7"}>{"Accelerate remediation "}</span>
                    {"prioritizing by Risk exposure."}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"space-between"}
                  pt={"10px"}
                >
                  <Text tone={"light"}>{"1/2"}</Text>
                  <Button onClick={goToFirstFinding} variant={"secondary"}>
                    {"Next"}
                  </Button>
                </Container>
              </Container>
            ),
            hideCloseButton: true,
            placement: "auto",
            styles: tourStyle,
            target: "#riskExposureColumn",
          },
        ]}
      />
    );
  }

  if (runRiskExposureTour && step === 2) {
    return (
      <Tour
        onFinish={finishTour}
        run={runRiskExposureTour}
        steps={[
          {
            ...BaseStep,
            content: (
              <Container>
                <Container align={"center"} display={"flex"} justify={"end"}>
                  <Button
                    icon={faClose}
                    id={"close-tour"}
                    onClick={finishTour}
                    variant={"secondary"}
                  />
                </Container>
                <Container pt={"10px"}>
                  <Text fw={7} mb={2} tone={"light"}>
                    {"% Risk exposure"}
                  </Text>
                  <Text tone={"light"}>
                    {`For example, decrease ${findingRiskExposure} of your Total Risk Exposure by fixing all the vulnerabilities of this type`}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"space-between"}
                  pt={"10px"}
                >
                  <Text tone={"light"}>{"2/2"}</Text>
                  <Button onClick={finishTour} variant={"secondary"}>
                    {"Close"}
                  </Button>
                </Container>
              </Container>
            ),
            hideCloseButton: true,
            placement: "auto",
            styles: tourStyle,
            target: "#riskExposureCard",
          },
        ]}
      />
    );
  }

  return <div />;
};

export { RiskExposureTour };
