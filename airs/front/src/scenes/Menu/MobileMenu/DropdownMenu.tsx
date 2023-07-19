/* eslint react/forbid-component-props: 0 */
/* eslint react/jsx-no-bind: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback, useState } from "react";
import {
  BsChevronLeft,
  BsChevronRight,
  BsFillPersonFill,
} from "react-icons/bs";
import { IoMdClose } from "react-icons/io";
import { useWindowSize } from "usehooks-ts";

import { Search } from "./Search";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { CloudImage } from "../../../components/CloudImage";
import { Container } from "../../../components/Container";
import type { TDisplay } from "../../../components/Container/types";
import { Text } from "../../../components/Typography";
import {
  NavbarInnerContainer,
  NavbarList,
} from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CompanyMenu } from "../Categories/Company";
import { PlatformMenu } from "../Categories/Platform";
import { ResourcesMenu } from "../Categories/Resources";
import { ServiceMenu } from "../Categories/Service";
import {
  ContainerWithSlide,
  MenuFootContainer,
  MenuMobileInnerContainer,
  SlideMenu,
} from "../styles/styledComponents";

interface IServiceProps {
  display: TDisplay;
  handleClick: () => void;
  status: number;
  setStatus: React.Dispatch<React.SetStateAction<number>>;
}

const DropdownMenu: React.FC<IServiceProps> = ({
  display,
  handleClick,
  status,
  setStatus,
}): JSX.Element => {
  const { width } = useWindowSize();
  const [categoryShowed, setCategoryShowed] = useState(0);
  const contents: JSX.Element[] = [
    <div key={"close"} />,
    <ServiceMenu display={"block"} key={"services"} />,
    <PlatformMenu display={"block"} key={"platform"} />,
    <ResourcesMenu display={"block"} key={"resources"} />,
    <CompanyMenu display={"block"} key={"company"} />,
  ];
  const categories: string[] = [
    "none",
    "Service",
    "Platform",
    "Resources",
    "Company",
  ];
  const searchIndices = [
    {
      description: `fluidattacks_airs`,
      keywords: `fluidattacks_airs`,
      name: `fluidattacks_airs`,
      title: `fluidattacks_airs`,
    },
  ];
  const handleClickButton = useCallback(
    (el: number): (() => void) =>
      (): void => {
        setStatus(2);
        setCategoryShowed(0);
        setCategoryShowed(el);
      },
    [setStatus]
  );

  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "navbar" });
  }, [trackEvent]);

  return (
    <MenuMobileInnerContainer
      style={{ display: width < 1240 ? display : "none" }}
    >
      <NavbarInnerContainer id={"inner_navbar"}>
        <NavbarList className={"poppins"} id={"navbar_list"}>
          <div className={"w-auto flex flex-nowrap"}>
            <li>
              <Link className={"db tc pa1 no-underline"} to={"/"}>
                <Container ph={3} pv={2} width={"160px"}>
                  <CloudImage
                    alt={"Fluid Attacks logo navbar"}
                    src={"airs/menu/Logo.png"}
                  />
                </Container>
              </Link>
            </li>
          </div>
          <Container
            display={width < 720 ? "none" : "flex"}
            justify={"end"}
            minWidth={"447px"}
            width={width > 1240 ? "auto" : "80%"}
            wrap={"nowrap"}
          >
            <AirsLink href={"/contact-us/"}>
              <Button variant={"tertiary"}>
                {translate.t("menu.buttons.contact")}
              </Button>
            </AirsLink>
            <Container maxWidth={"142px"} ml={2} mr={2}>
              <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                  {translate.t("menu.buttons.trial")}
                </Button>
              </AirsLink>
            </Container>
            <AirsLink href={"https://app.fluidattacks.com/"}>
              <Button variant={"ghost"}>
                <BsFillPersonFill />
                {translate.t("menu.buttons.login")}
              </Button>
            </AirsLink>
          </Container>
          <Container
            display={width < 1241 ? "flex" : "none"}
            justify={"center"}
            justifyMd={"end"}
            justifySm={"end"}
            maxWidth={width > 720 ? "50px" : "90%"}
          >
            <Button onClick={handleClick} variant={"ghost"}>
              <IoMdClose size={width > 960 ? 20 : 25} />
            </Button>
          </Container>
        </NavbarList>
      </NavbarInnerContainer>

      <Container
        bgColor={"#ffffff"}
        display={width < 1201 ? display : "none"}
        height={"50%"}
        position={"absolute"}
        width={"100%"}
      >
        <SlideMenu isShown={categoryShowed === 0} status={status}>
          <Search indices={searchIndices} />
          <Container width={"auto"} widthSm={"100%"}>
            <Button
              customSize={{
                fontSize: 16,
                ph: 32,
                pv: 10,
              }}
              display={"block"}
              onClick={handleClickButton(1)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {translate.t("menu.buttons.service")}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
          <Container width={"auto"} widthSm={"100%"}>
            <Button
              customSize={{
                fontSize: 16,
                ph: 32,
                pv: 10,
              }}
              display={"block"}
              onClick={handleClickButton(2)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {translate.t("menu.buttons.platform")}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
          <AirsLink href={"/plans/"}>
            <Container width={"auto"} widthSm={"100%"}>
              <Button
                customSize={{
                  fontSize: 16,
                  ph: 32,
                  pv: 10,
                }}
                display={"block"}
                onClick={handleClick}
                variant={"ghost"}
              >
                <Container display={"flex"} width={"100%"}>
                  <Container width={"98%"}>
                    <Text
                      color={"#2e2e38"}
                      display={"inline"}
                      textAlign={"start"}
                    >
                      {translate.t("menu.buttons.plans")}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
          </AirsLink>

          <Container width={"auto"} widthSm={"100%"}>
            <Button
              customSize={{
                fontSize: 16,
                ph: 32,
                pv: 10,
              }}
              display={"block"}
              onClick={handleClickButton(3)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {translate.t("menu.buttons.resources")}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
          <AirsLink href={"/advisories/"}>
            <Container width={"auto"} widthSm={"100%"}>
              <Button
                customSize={{
                  fontSize: 16,
                  ph: 32,
                  pv: 10,
                }}
                display={"block"}
                onClick={handleClick}
                variant={"ghost"}
              >
                <Container display={"flex"} width={"100%"}>
                  <Container width={"98%"}>
                    <Text
                      color={"#2e2e38"}
                      display={"inline"}
                      textAlign={"start"}
                    >
                      {translate.t("menu.buttons.advisories")}
                    </Text>
                  </Container>
                </Container>
              </Button>
            </Container>
          </AirsLink>

          <Container width={"auto"} widthSm={"100%"}>
            <Button
              customSize={{
                fontSize: 16,
                ph: 32,
                pv: 10,
              }}
              display={"block"}
              onClick={handleClickButton(4)}
              variant={"ghost"}
            >
              <Container display={"flex"} width={"100%"}>
                <Container width={"98%"}>
                  <Text
                    color={"#2e2e38"}
                    display={"inline"}
                    textAlign={"start"}
                  >
                    {translate.t("menu.buttons.company")}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  minWidth={"25px"}
                  width={"2%"}
                >
                  <BsChevronRight color={"#2e2e38"} size={16} />
                </Container>
              </Container>
            </Button>
          </Container>
        </SlideMenu>
        <MenuFootContainer id={"menufoot"} isShown={true}>
          <Container
            align={"center"}
            bgColor={"#aaaaa"}
            display={"flex"}
            justify={"center"}
            width={"100%"}
          >
            <Container
              align={"center"}
              display={width < 728 ? "flex" : "none"}
              justify={"center"}
            >
              <Container
                align={"center"}
                display={"block"}
                justify={"center"}
                width={"90%"}
                wrap={"nowrap"}
              >
                <AirsLink href={"/contact-us/"}>
                  <Button display={"block"} variant={"tertiary"}>
                    {translate.t("menu.buttons.contact")}
                  </Button>
                </AirsLink>
                <br />
                <AirsLink
                  decoration={"none"}
                  href={"https://app.fluidattacks.com/SignUp"}
                >
                  <Button
                    display={"block"}
                    onClick={matomoFreeTrialEvent}
                    variant={"primary"}
                  >
                    {translate.t("menu.buttons.trial")}
                  </Button>
                </AirsLink>
              </Container>
            </Container>
          </Container>
        </MenuFootContainer>
        <ContainerWithSlide isShown={categoryShowed !== 0}>
          <Container borderBottomColor={"#2e2e38"} mb={3}>
            <Button
              customSize={{
                fontSize: 16,
                ph: 30,
                pv: 10,
              }}
              icon={
                <BsChevronLeft
                  color={"#2e2e38"}
                  size={16}
                  style={{ paddingRight: "10px" }}
                />
              }
              iconSide={"left"}
              onClick={handleClickButton(0)}
              variant={"ghost"}
            >
              {categories[categoryShowed]}
            </Button>
          </Container>
          {contents[categoryShowed]}
        </ContainerWithSlide>
      </Container>
    </MenuMobileInnerContainer>
  );
};

export { DropdownMenu };
