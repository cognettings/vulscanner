import React from "react";
import { useTranslation } from "react-i18next";

import { IconBlock } from "./styledComponents";

import { CloudImage } from "../../../../components/CloudImage";
import { Container } from "../../../../components/Container";
import { Grid } from "../../../../components/Grid";
import { Text, Title } from "../../../../components/Typography";

const ContinuousHackingToolsMedium: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

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
          {t("continuousHackingPage.tools.title")}
        </Title>
      </Container>
      <Container
        display={"flex"}
        justify={"center"}
        maxWidth={"1290px"}
        pt={3}
        wrap={"wrap"}
      >
        <CloudImage
          alt={"tools-image"}
          src={"airs/services/continuous-hacking/tools/order-medium.png"}
        />
        <Grid columns={4} gap={"1rem"} pv={"60px"}>
          <Container>
            <Title
              color={"#2e2e38"}
              level={2}
              mb={4}
              size={"xs"}
              textAlign={"start"}
            >
              {t("continuousHackingPage.tools.types.1.title")}
            </Title>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/identification1.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.1.1.title")}
                </Text>
                <Text color={"#40404f"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.1.1.subtitle")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/identification2.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.1.2")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/identification3.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.1.3.title")}
                </Text>
                <Text color={"#40404f"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.1.3.subtitle")}
                </Text>
              </Container>
            </Container>
          </Container>
          <Container>
            <Title
              color={"#2e2e38"}
              level={2}
              mb={4}
              size={"xs"}
              textAlign={"start"}
            >
              {t("continuousHackingPage.tools.types.2.title")}
            </Title>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={"airs/services/continuous-hacking/tools/review1.png"}
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.2.1")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={"airs/services/continuous-hacking/tools/review2.png"}
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.2.2")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={"airs/services/continuous-hacking/tools/review3.png"}
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.2.3")}
                </Text>
              </Container>
            </Container>
          </Container>
          <Container>
            <Title
              color={"#2e2e38"}
              level={2}
              mb={5}
              size={"xs"}
              textAlign={"start"}
            >
              {t("continuousHackingPage.tools.types.3.title")}
            </Title>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/remediation1.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.3.1")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/remediation2.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.3.2")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/remediation3.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.3.3")}
                </Text>
              </Container>
            </Container>
          </Container>
          <Container>
            <Title
              color={"#2e2e38"}
              level={2}
              mb={4}
              size={"xs"}
              textAlign={"start"}
            >
              {t("continuousHackingPage.tools.types.4.title")}
            </Title>
            <Container align={"center"} display={"flex"} mv={4}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/verification1.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.4.1")}
                </Text>
              </Container>
            </Container>
            <Container align={"center"} display={"flex"}>
              <IconBlock>
                <CloudImage
                  alt={"tools-image"}
                  src={
                    "airs/services/continuous-hacking/tools/verification2.png"
                  }
                />
              </IconBlock>
              <Container display={"flex"} wrap={"wrap"}>
                <Text color={"#25252d"} display={"inline-block"} size={"xs"}>
                  {t("continuousHackingPage.tools.types.4.2")}
                </Text>
              </Container>
            </Container>
          </Container>
        </Grid>
      </Container>
    </Container>
  );
};

export { ContinuousHackingToolsMedium };
