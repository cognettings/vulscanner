import { faCheckCircle } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import type { FC } from "react";

import type { IStepLapseProps } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Text } from "components/Text";

const StepLapse: FC<IStepLapseProps> = ({
  finalButtonText,
  finalButtonType = "button",
  finalClick,
  isDisabledFinalButton,
  steps,
}): JSX.Element => {
  const [currentStep, setCurrentStep] = useState(1);

  const nextStep = useCallback((): void => {
    setCurrentStep(currentStep + 1);
  }, [currentStep]);

  const previousStep = useCallback((): void => {
    setCurrentStep(currentStep - 1);
  }, [currentStep]);

  return (
    <Container>
      {steps.map((step, index): JSX.Element => {
        const { nextAction, previousAction } = step;

        function next(): void {
          nextStep();
          if (!_.isUndefined(nextAction)) {
            nextAction();
          }
        }

        function previous(): void {
          previousStep();
          if (!_.isUndefined(previousAction)) {
            previousAction();
          }
        }

        return (
          <Container display={"flex"} key={step.title} scroll={"none"}>
            <Container
              display={"flex"}
              height={"auto"}
              justify={"center"}
              scroll={"none"}
              width={"24px"}
              wrap={"wrap"}
            >
              <Container
                align={"center"}
                bgColor={`${currentStep >= index + 1 ? "#BF0B1A" : "#f4f4f6"}`}
                border={`1px solid ${
                  currentStep >= index + 1 ? "#BF0B1A" : "#B0B0BF"
                }`}
                br={"2px"}
                display={"flex"}
                height={"24px"}
                scroll={"none"}
                width={"100%"}
              >
                <Text
                  bright={currentStep >= index + 1 ? 1 : 7}
                  fw={7}
                  size={"small"}
                  ta={"center"}
                  tone={"light"}
                >
                  {currentStep > index + 1 ? (
                    <FontAwesomeIcon icon={faCheckCircle} />
                  ) : (
                    index + 1
                  )}
                </Text>
              </Container>
              {index + 1 - steps.length === 0 ? (
                <div />
              ) : (
                <Container
                  bgColor={currentStep > index + 1 ? "#BF0B1A" : "#E9E9ED"}
                  height={"100%"}
                  width={"2px"}
                />
              )}
            </Container>
            <Container pl={"8px"} width={"100%"}>
              <Container
                align={"center"}
                display={"flex"}
                height={"24px"}
                scroll={"none"}
              >
                <Text fw={7} size={"small"}>
                  {step.title}
                </Text>
              </Container>
              <Container pb={"24px"} pt={"24px"}>
                {currentStep === index + 1 ? (
                  <Container>
                    <Container scroll={"none"}>{step.content}</Container>
                    <Container display={"flex"} margin={"14px 0 0 0"}>
                      {currentStep > 1 ? (
                        <Container margin={"0 8px 0 0"}>
                          <Button
                            disabled={step.isDisabledPrevious ?? false}
                            onClick={previous}
                            variant={"tertiary"}
                          >
                            {"Previous"}
                          </Button>
                        </Container>
                      ) : undefined}
                      {currentStep - steps.length === 0 ? (
                        <Button
                          disabled={isDisabledFinalButton ?? false}
                          onClick={finalClick}
                          type={finalButtonType}
                          variant={"primary"}
                        >
                          {finalButtonText}
                        </Button>
                      ) : (
                        <Button
                          disabled={step.isDisabledNext ?? false}
                          onClick={next}
                          variant={"primary"}
                        >
                          {"Next step"}
                        </Button>
                      )}
                    </Container>
                  </Container>
                ) : undefined}
              </Container>
            </Container>
          </Container>
        );
      })}
    </Container>
  );
};

export { StepLapse };
