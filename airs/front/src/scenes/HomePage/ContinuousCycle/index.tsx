/* eslint fp/no-mutation:0 */
import React, { useCallback, useEffect, useState } from "react";
import {
  BsChevronDown,
  BsChevronUp,
  BsFillArrowLeftCircleFill,
  BsFillArrowRightCircleFill,
} from "react-icons/bs";

import {
  DescriptionCard,
  DropdownBar,
  ProgressBar,
  ScrollButton,
  SlideHook,
  SlideShow,
  SplitBar,
} from "./styledComponents";

import { Button } from "../../../components/Button";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import { Grid } from "../../../components/Grid";
import { Text, Title } from "../../../components/Typography";
import { useCarrousel } from "../../../utils/hooks";
import { useWindowSize } from "../../../utils/hooks/useWindowSize";
import { i18next, translate } from "../../../utils/translations/translate";

const ContinuousCycle: React.FC = (): JSX.Element => {
  const { width } = useWindowSize();
  const [state, setState] = useState(0);
  const [isSelected, setIsSelected] = useState(false);
  const imageLanguage = i18next.language === "es" ? "/es" : "";
  const screen = width > 960 ? "big" : "md";

  const timePerProgress = 80;
  const numberOfCycles = 6;
  const { cycle, progress } = useCarrousel(
    timePerProgress,
    numberOfCycles,
    isSelected,
    state
  );

  const cardWidth = width * 0.63;
  const maxScroll = cardWidth * 7;

  const [currentWidth, setCurrentWidth] = useState(0);
  const [scroll, setScroll] = useState(0);
  // For mobile view
  const scrollLeft: () => void = useCallback((): void => {
    setState(state - 1);
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  }, [cardWidth, state, scroll]);

  const scrollRight: () => void = useCallback((): void => {
    setState(state + 1);
    setScroll(
      scroll > currentWidth - cardWidth ? currentWidth : scroll + cardWidth
    );
  }, [scroll, currentWidth, cardWidth, state]);

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < currentWidth) {
      element.scrollLeft = scroll;
    } else {
      element.scrollLeft += 0;
    }
    setCurrentWidth(maxScroll - element.offsetWidth);
  };

  useEffect((): void => {
    const slideShow: HTMLElement = document.getElementById(
      "solutionsSlides"
    ) as HTMLElement;
    changeScroll(slideShow);
  });

  // For desktop view
  const getProgress = useCallback(
    (el: number): string => {
      if (cycle > el) {
        return "100%";
      }

      return cycle === el ? `${progress}%` : "0%";
    },
    [cycle, progress]
  );

  useEffect((): void => {
    if (screen === "big") {
      setState(cycle);
    }
  }, [cycle, screen]);

  const cycleIncomplete = useCallback(
    (el: number): boolean => {
      const actProgress = getProgress(el);

      return actProgress !== "100%" && cycle === el;
    },
    [cycle, getProgress]
  );

  const handleClick = useCallback(
    (el: number): (() => void) =>
      (): void => {
        setState(el);
        setIsSelected(true);
      },
    []
  );

  if (screen === "md") {
    return (
      <Container bgColor={"#ffffff"}>
        <Container display={"flex"} justify={"end"}>
          <Container
            align={"center"}
            display={"flex"}
            justify={"end"}
            maxWidth={"1420px"}
            mr={0}
            wrap={"wrap"}
          >
            <Container ph={4} pv={5} width={"70%"} widthMd={"100%"}>
              <Title color={"#bf0b1a"} level={3} mb={3} size={"small"}>
                {translate.t("home.continuousCycle.subtitle")}
              </Title>
              <Title color={"#11111"} level={1} size={"medium"}>
                {translate.t("home.continuousCycle.title")}
              </Title>
            </Container>
            <div style={{ width: "30%" }} />
          </Container>
        </Container>
        <Grid columns={1} columnsMd={1} columnsSm={1} gap={"3rem"}>
          <Container
            align={"center"}
            center={true}
            display={"flex"}
            justify={"center"}
          >
            <Container maxWidth={"80%"}>
              <CloudImage
                alt={"cycle-image"}
                src={`airs${imageLanguage}/home/ContinuousCycle/ciclo-hc-fluid-${state}-update.png`}
              />
            </Container>
          </Container>
          <SlideShow id={"solutionsSlides"}>
            {[...Array(6).keys()].map(
              (el: number): JSX.Element => (
                <Container
                  bgColor={"#ffffff"}
                  key={`cycle${el}`}
                  maxWidth={"97%"}
                  minHeight={"100px"}
                  minWidth={"70%"}
                  pr={state === 5 ? 1 : 0}
                >
                  <Container pl={3}>
                    <Title color={"#2e2e38"} level={4} size={"small"}>
                      {translate.t(`home.continuousCycle.cycle${el}.title`)}
                    </Title>
                    <Text color={"#535365"}>
                      {translate.t(`home.continuousCycle.cycle${el}.subtitle`)}
                    </Text>
                  </Container>
                </Container>
              )
            )}
          </SlideShow>
        </Grid>
        <Container display={"flex"} justify={"center"} pb={2} wrap={"wrap"}>
          <ScrollButton>
            <Button
              disabled={state === 0}
              onClick={scrollLeft}
              size={"lg"}
              variant={"transparent"}
            >
              <BsFillArrowLeftCircleFill color={"#40404f"} size={50} />
            </Button>
            <Button
              disabled={state === 5}
              onClick={scrollRight}
              variant={"transparent"}
            >
              <BsFillArrowRightCircleFill color={"#40404f"} size={50} />
            </Button>
          </ScrollButton>
        </Container>
      </Container>
    );
  }

  return (
    <Container bgColor={"#ffffff"} justify={"center"} ph={6} pv={5}>
      <Container
        align={"center"}
        bgColor={"#ffffff"}
        center={true}
        display={"flex"}
        justify={"center"}
        maxWidth={"1440px"}
        wrap={"wrap"}
      >
        <Container display={"flex"} justify={"end"}>
          <Container
            align={"center"}
            display={"flex"}
            justify={"end"}
            maxWidth={"1420px"}
            mr={0}
            wrap={"wrap"}
          >
            <Container pv={5} width={"70%"} widthMd={"100%"}>
              <Title color={"#bf0b1a"} level={3} mb={3} size={"small"}>
                {translate.t("home.continuousCycle.subtitle")}
              </Title>
              <Title color={"#11111"} level={1} size={"medium"}>
                {translate.t("home.continuousCycle.title")}
              </Title>
            </Container>
            <div style={{ width: "30%" }} />
          </Container>
        </Container>
        <Grid columns={2} columnsMd={1} columnsSm={1} gap={"7rem"}>
          <Container display={"flex"} justify={"center"} pv={5} wrap={"wrap"}>
            {[...Array(6).keys()].map(
              (el: number): JSX.Element => (
                <DropdownBar key={`cycle${el}`}>
                  <SlideHook id={"solutionsSlides"} />
                  {cycleIncomplete(el) ? (
                    <Container
                      bgColor={"#DDDDE3"}
                      height={"4px"}
                      width={"100%"}
                    >
                      <ProgressBar width={getProgress(el)} />
                    </Container>
                  ) : (
                    <SplitBar />
                  )}
                  <Button
                    icon={
                      cycleIncomplete(el) ? (
                        <BsChevronUp size={12} />
                      ) : (
                        <BsChevronDown size={12} />
                      )
                    }
                    iconSide={"right"}
                    onClick={handleClick(el)}
                    variant={"transparent"}
                  >
                    <Title
                      color={"#2e2e38"}
                      level={2}
                      size={"small"}
                      textAlign={"start"}
                    >
                      {translate.t(`home.continuousCycle.cycle${el}.title`)}
                    </Title>
                  </Button>
                  <DescriptionCard isCycleIncomplete={cycleIncomplete(el)}>
                    <Container justify={"start"} width={"95%"} wrap={"wrap"}>
                      <Text color={"#535365"} mb={3} ml={3} mt={1}>
                        {translate.t(
                          `home.continuousCycle.cycle${el}.subtitle`
                        )}
                      </Text>
                    </Container>
                  </DescriptionCard>
                  {el === numberOfCycles - 1 ? <SplitBar /> : undefined}
                </DropdownBar>
              )
            )}
          </Container>
          <Container align={"center"} display={"flex"}>
            <Container>
              <CloudImage
                alt={"cycle-image"}
                src={`airs${imageLanguage}/home/ContinuousCycle/ciclo-hc-fluid-${cycle}-update.png`}
              />
            </Container>
          </Container>
        </Grid>
      </Container>
    </Container>
  );
};

export { ContinuousCycle };
