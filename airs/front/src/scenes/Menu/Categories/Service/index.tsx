import React, { useCallback } from "react";
import { useWindowSize } from "usehooks-ts";

import { AirsLink } from "../../../../components/AirsLink";
import { Container } from "../../../../components/Container";
import type { TDisplay } from "../../../../components/Container/types";
import { Grid } from "../../../../components/Grid";
import { Text } from "../../../../components/Typography";
import { translate } from "../../../../utils/translations/translate";

interface IServiceProps {
  display: TDisplay;
}

const ServiceMenu: React.FC<IServiceProps> = ({
  display,
}: IServiceProps): JSX.Element => {
  const { width } = useWindowSize();
  const handleClick = useCallback((): void => {
    document.body.setAttribute("style", "overflow-y: auto;");
  }, []);

  return (
    <Container
      bgColor={"#ffffff"}
      display={display}
      shadowBottom={width > 1240}
    >
      <Container
        display={width > 960 ? "flex" : "block"}
        height={"max-content"}
        justify={"center"}
        mb={3}
      >
        <Container
          maxWidth={width > 960 ? "457px" : "1440px"}
          ph={4}
          scroll={"y"}
        >
          <Container
            borderBottomColor={"#dddde3"}
            height={"36px"}
            mb={3}
            pb={3}
          >
            <Text color={"#8f8fa3"} size={"xs"}>
              {translate.t("menu.services.allInOne.title")}
            </Text>
          </Container>
          <Container>
            <AirsLink
              hovercolor={"#bf0b1a"}
              href={"/services/continuous-hacking/"}
              onClick={handleClick}
            >
              <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                {translate.t("menu.services.allInOne.continuous.title")}
              </Text>
            </AirsLink>
            <Text color={"#535365"} mb={3} size={"xs"}>
              {translate.t("menu.services.allInOne.continuous.subtitle")}
            </Text>
          </Container>
        </Container>
        <Container maxWidth={width > 960 ? "832px" : "1440px"} ph={4}>
          <Container borderBottomColor={"#dddde3"} height={"36px"} pb={3}>
            <Text color={"#8f8fa3"} size={"xs"}>
              {translate.t("menu.services.solutions.title")}
            </Text>
          </Container>
          <Grid columns={2} columnsMd={1} columnsSm={1} gap={"1rem"} ph={"0px"}>
            <Container>
              <AirsLink
                hovercolor={"#bf0b1a"}
                href={"/solutions/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.services.solutions.applicationSec.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"xs"}>
                {translate.t("menu.services.solutions.applicationSec.subtitle")}
              </Text>
            </Container>
            <Container>
              <AirsLink
                hovercolor={"#bf0b1a"}
                href={"/compliance/"}
                onClick={handleClick}
              >
                <Text color={"#2e2e38"} mb={3} size={"small"} weight={"bold"}>
                  {translate.t("menu.services.solutions.compliance.title")}
                </Text>
              </AirsLink>
              <Text color={"#535365"} size={"xs"}>
                {translate.t("menu.services.solutions.compliance.subtitle")}
              </Text>
            </Container>
          </Grid>
        </Container>
      </Container>
    </Container>
  );
};

export { ServiceMenu };
