import {
  faChevronRight,
  faCircleExclamation,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  machineLanguages,
  squadCICD,
  squadInfra,
  squadLanguages,
} from "./utils";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { ExternalLink } from "components/ExternalLink";
import { List } from "components/List";
import { SidePanel } from "components/SidePanel";
import { Text } from "components/Text";

export const LanguagesButton: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const [machinePanel, setMachinePanel] = useState(false);
  const openMachinePanel = useCallback((): void => {
    mixpanel.track("SupportedLanguagesOnboarding");
    setMachinePanel(true);
  }, []);
  const closeMachinePanel = useCallback((): void => {
    setMachinePanel(false);
  }, []);
  const [squadPanel, setSquadPanel] = useState(false);
  const openSquadPanel = useCallback((): void => {
    setSquadPanel(true);
  }, []);
  const closeSquadPanel = useCallback((): void => {
    setSquadPanel(false);
    setMachinePanel(false);
  }, []);

  const renderMachineUtil = useCallback((language: string): JSX.Element => {
    return (
      <Container align={"start"} pb={"7px"} pt={"7px"}>
        <Text bright={3} fontSize={"16px"} ta={"start"} tone={"dark"}>
          {language}
        </Text>
      </Container>
    );
  }, []);

  const renderSquadUtil = useCallback((language: string): JSX.Element => {
    return (
      <Container align={"start"} pb={"3px"} pt={"3px"}>
        <Text bright={3} fontSize={"16px"} ta={"start"} tone={"dark"}>
          {language}
        </Text>
      </Container>
    );
  }, []);

  return (
    <Container align={"center"} display={"flex"} justify={"center"}>
      <Button
        icon={faCircleExclamation}
        onClick={openMachinePanel}
        textDecoration={"underline"}
      >
        {t("autoenrollment.languages.checkLanguages")}
      </Button>
      <Container pl={"5px"}>
        <SidePanel
          bgBlocked={true}
          onClose={closeMachinePanel}
          open={machinePanel}
          width={"520px"}
        >
          <Container scrollInvisible={true}>
            <Container borderBottom={"2px solid #dddde3"} pb={"10px"}>
              <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                {t("autoenrollment.languages.machineLanguages.title")}
              </Text>
            </Container>
            <Container
              align={"center"}
              display={"flex"}
              pt={"32px"}
              ptMd={"12px"}
              wrap={"wrap"}
            >
              <Container pr={"8px"}>
                <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                  {t("autoenrollment.languages.machineLanguages.machinePlan")}
                </Text>
              </Container>
              <Container
                align={"center"}
                border={"solid 1px #2e2e38"}
                borderBL={"12px"}
                borderBR={"12px"}
                borderTR={"12px"}
                borderTl={"12px"}
                display={"flex"}
                height={"26px"}
                justify={"center"}
                width={"75px"}
              >
                <Text bright={3} fontSize={"12px"} ta={"center"} tone={"dark"}>
                  {t("autoenrollment.languages.machineLanguages.tag")}
                </Text>
              </Container>
              <Container
                lineHeight={"1.5"}
                pb={"70px"}
                pbMd={"10px"}
                pt={"14px"}
                ptMd={"5px"}
              >
                <Text bright={3} fontSize={"16px"} tone={"dark"}>
                  {t("autoenrollment.languages.machineLanguages.description")}
                </Text>
              </Container>
              <Container
                bgColor={"#ffffff"}
                borderBL={"5px"}
                borderBR={"5px"}
                borderTR={"5px"}
                borderTl={"5px"}
                height={"370px"}
                width={"470px"}
              >
                <Container pb={"20px"} pl={"20px"} pr={"20px"} pt={"20px"}>
                  <List
                    columns={2}
                    items={machineLanguages}
                    justify={"start"}
                    render={renderMachineUtil}
                  />
                </Container>
              </Container>
              <Container pt={"70px"} ptMd={"10px"}>
                <Button onClick={closeMachinePanel} variant={"primary"}>
                  {t("autoenrollment.languages.machineLanguages.button")}
                </Button>
              </Container>
              <Container pt={"10px"}>
                <Button onClick={openSquadPanel} variant={"carousel"}>
                  <Text disp={"inline"}>
                    {t(
                      "autoenrollment.languages.machineLanguages.buttonSquadLanguages"
                    )}
                    <Text bright={3} disp={"inline"} fw={9} tone={"dark"}>
                      <ExternalLink>
                        {t(
                          "autoenrollment.languages.machineLanguages.checkSquadLanguages"
                        )}
                      </ExternalLink>
                    </Text>
                    <FontAwesomeIcon icon={faChevronRight} />
                  </Text>
                </Button>
              </Container>
            </Container>
          </Container>
        </SidePanel>
        <SidePanel onClose={closeSquadPanel} open={squadPanel} width={"940px"}>
          <Container display={"flex"} scrollInvisible={true} wrap={"wrap"}>
            <Container
              borderBottom={"2px solid #dddde3"}
              pb={"10px"}
              width={"100%"}
            >
              <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                {t("autoenrollment.languages.machineLanguages.title")}
              </Text>
            </Container>
            <Container width={"50%"}>
              <Container
                align={"center"}
                display={"flex"}
                pt={"32px"}
                wrap={"wrap"}
              >
                <Container pr={"8px"}>
                  <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                    {t("autoenrollment.languages.machineLanguages.machinePlan")}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  border={"solid 1px #2e2e38"}
                  borderBL={"12px"}
                  borderBR={"12px"}
                  borderTR={"12px"}
                  borderTl={"12px"}
                  display={"flex"}
                  height={"26px"}
                  justify={"center"}
                  width={"75px"}
                >
                  <Text
                    bright={3}
                    fontSize={"12px"}
                    ta={"center"}
                    tone={"dark"}
                  >
                    {t("autoenrollment.languages.machineLanguages.tag")}
                  </Text>
                </Container>
                <Container lineHeight={"1.5"} pb={"85px"} pt={"14px"}>
                  <Text bright={3} fontSize={"16px"} tone={"dark"}>
                    {t("autoenrollment.languages.machineLanguages.description")}
                  </Text>
                </Container>
                <Container
                  bgColor={"#ffffff"}
                  borderBL={"5px"}
                  borderBR={"5px"}
                  borderTR={"5px"}
                  borderTl={"5px"}
                  height={"370px"}
                  scroll={"none"}
                  width={"400px"}
                >
                  <Container pb={"20px"} pl={"20px"} pr={"20px"} pt={"20px"}>
                    <List
                      columns={2}
                      items={machineLanguages}
                      justify={"start"}
                      render={renderMachineUtil}
                    />
                  </Container>
                </Container>
                <Container pt={"110px"}>
                  <Button onClick={closeSquadPanel} variant={"primary"}>
                    {t("autoenrollment.languages.machineLanguages.button")}
                  </Button>
                </Container>
              </Container>
            </Container>
            <Container width={"50%"}>
              <Container
                align={"center"}
                display={"flex"}
                pt={"32px"}
                wrap={"wrap"}
              >
                <Container pr={"8px"}>
                  <Text bright={3} fw={9} size={"big"} tone={"dark"}>
                    {t("autoenrollment.languages.squadLanguages.squadPlan")}
                  </Text>
                </Container>
                <Container lineHeight={"1.5"} pb={"25px"} pt={"14px"}>
                  <Text bright={3} fontSize={"16px"} tone={"dark"}>
                    {t("autoenrollment.languages.squadLanguages.description")}
                  </Text>
                </Container>
                <Container lineHeight={"1.5"} pb={"12px"} pt={"0px"}>
                  <Text bright={3} fontSize={"16px"} fw={9} tone={"dark"}>
                    {t("autoenrollment.languages.squadLanguages.description2")}
                  </Text>
                </Container>
                <Container
                  bgColor={"#ffffff"}
                  borderBL={"5px"}
                  borderBR={"5px"}
                  borderTR={"5px"}
                  borderTl={"5px"}
                  height={"435px"}
                  width={"400px"}
                >
                  <Container pb={"20px"} pl={"20px"} pr={"20px"} pt={"20px"}>
                    <List
                      columns={3}
                      items={squadLanguages}
                      justify={"start"}
                      render={renderSquadUtil}
                    />
                    <Container pb={"10px"} pt={"10px"}>
                      <Text bright={3} fontSize={"20px"} fw={9} tone={"dark"}>
                        {t(
                          "autoenrollment.languages.squadLanguages.squadSupportedCICD"
                        )}
                      </Text>
                    </Container>
                    <List
                      columns={2}
                      items={squadCICD}
                      justify={"start"}
                      render={renderSquadUtil}
                    />
                    <Container pb={"10px"} pt={"10px"}>
                      <Text bright={3} fontSize={"20px"} fw={9} tone={"dark"}>
                        {t(
                          "autoenrollment.languages.squadLanguages.squadSupportedInfra"
                        )}
                      </Text>
                    </Container>
                    <List
                      columns={2}
                      items={squadInfra}
                      justify={"start"}
                      render={renderSquadUtil}
                    />
                  </Container>
                </Container>
                <Container pt={"40px"}>
                  <ExternalLink href={"https://fluidattacks.com/contact-us/"}>
                    <Button variant={"tertiary"}>
                      {t("autoenrollment.languages.squadLanguages.button")}
                    </Button>
                  </ExternalLink>
                </Container>
              </Container>
            </Container>
          </Container>
        </SidePanel>
      </Container>
    </Container>
  );
};
