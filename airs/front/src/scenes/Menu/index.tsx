/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, {
  createRef,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";
import type { RefObject } from "react";
import { BsFillPersonFill } from "react-icons/bs";
import { FiMenu } from "react-icons/fi";
import { useWindowSize } from "usehooks-ts";

import { CompanyMenu } from "./Categories/Company";
import { PlatformMenu } from "./Categories/Platform";
import { ResourcesMenu } from "./Categories/Resources";
import { ServiceMenu } from "./Categories/Service";
import { LanguageSwitcher } from "./Language/LanguageSwitcher";
import { DropdownMenu } from "./MobileMenu/DropdownMenu";
import { useClickOutside } from "./MobileMenu/Search/useClickOutside";
import { LoginButton, NavbarContainer } from "./styles/styledComponents";

import { AirsLink } from "../../components/AirsLink";
import { Button } from "../../components/Button";
import type { TDirection } from "../../components/Chevron";
import { Chevron } from "../../components/Chevron";
import { CloudImage } from "../../components/CloudImage";
import { Container } from "../../components/Container";
import {
  NavbarInnerContainer,
  NavbarList,
} from "../../styles/styledComponents";
import { i18next, translate } from "../../utils/translations/translate";
import type { ISize } from "components/Button/types";

export const NavbarComponent: React.FC = (): JSX.Element => {
  const { trackEvent } = useMatomo();
  const { width } = useWindowSize();
  const [menuStatus, setMenuStatus] = useState(0);
  const [categoryShown, setCategoryShown] = useState(0);
  const [isSecondaryMenuVisible, setIsSecondaryMenuVisible] = useState(true);

  const initialChevronStates = useMemo((): Record<string, TDirection> => {
    return {
      company: "down",
      platform: "down",
      resources: "down",
      services: "down",
    };
  }, []);
  const [chevrons, setChevrons] = useState(initialChevronStates);

  const customOptionsButtonSize: ISize = {
    fontSize: 16,
    ph: 9,
    pv: 10,
  };

  const handleScreen = useCallback((): string => {
    if (width < 1200 && width > 720) {
      return "medium";
    } else if (width < 720 && width > 10) {
      return "mobile";
    }

    return "desktop";
  }, [width]);
  const screen = handleScreen();
  const resetState = useCallback((): void => {
    setCategoryShown(0);
  }, []);
  const alternateChevron = useCallback(
    (category: string): void => {
      const alternativeChevron = chevrons[category] === "up" ? "down" : "up";
      setChevrons({ ...initialChevronStates, [category]: alternativeChevron });
    },
    [initialChevronStates, chevrons]
  );
  const resetChevrons = useCallback((): void => {
    setChevrons(initialChevronStates);
  }, [initialChevronStates]);
  const [menu, setMenu] = useState(false);
  const menuRef: RefObject<HTMLDivElement> = createRef();

  const handleClick = useCallback((): void => {
    setMenuStatus(menuStatus === 0 ? 1 : 0);
    setMenu(!menu);
    if (menu) {
      document.body.setAttribute("style", "overflow-y: auto;");
    } else {
      document.body.setAttribute("style", "overflow-y: hidden;");
    }
  }, [menu, menuStatus]);
  const contents: JSX.Element[] = [
    <div key={"close"} />,
    <ServiceMenu display={"block"} key={"services"} />,
    <PlatformMenu display={"block"} key={"platform"} />,
    <ResourcesMenu display={"block"} key={"resources"} />,
    <CompanyMenu display={"block"} key={"company"} />,
  ];
  const handleClickButton = useCallback(
    (category: string): (() => void) =>
      (): void => {
        resetState();
        alternateChevron(category);
        if (category === "services" && categoryShown !== 1) {
          setCategoryShown(1);
        } else if (category === "resources" && categoryShown !== 3) {
          setCategoryShown(3);
        } else if (category === "platform" && categoryShown !== 2) {
          setCategoryShown(2);
        } else if (category === "company" && categoryShown !== 4) {
          setCategoryShown(4);
        }
      },
    [resetState, alternateChevron, categoryShown]
  );
  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({ action: "free-trial-click", category: "navbar" });
  }, [trackEvent]);

  useClickOutside(menuRef, (): void => {
    resetState();
    resetChevrons();
  });
  const listenToScroll = useCallback((): void => {
    const heightToShowMenu = 0;
    const heightToHideMenu = 30;
    const winScroll =
      document.body.scrollTop || document.documentElement.scrollTop;

    if (winScroll === heightToShowMenu) {
      setIsSecondaryMenuVisible(true);
    } else if (winScroll >= heightToHideMenu) {
      setIsSecondaryMenuVisible(false);
    }
  }, []);

  useEffect((): (() => void) => {
    window.addEventListener("scroll", listenToScroll);

    return (): void => {
      window.removeEventListener("scroll", listenToScroll);
    };
  }, [listenToScroll]);
  handleScreen();

  if (screen === "mobile") {
    return (
      <NavbarContainer id={"navbar"} ref={menuRef}>
        <NavbarInnerContainer id={"inner_navbar"}>
          <NavbarList className={"poppins"} id={"navbar_list"}>
            <div className={"w-auto flex flex-nowrap"}>
              <li>
                <AirsLink href={"/"}>
                  <Container display={"block"} ph={3} pv={2} width={"160px"}>
                    <CloudImage
                      alt={"Fluid Attacks logo navbar"}
                      src={"airs/menu/Logo.png"}
                    />
                  </Container>
                </AirsLink>
              </li>
            </div>
            <Container
              align={"center"}
              display={"flex"}
              justify={"center"}
              justifyMd={"end"}
              justifySm={"end"}
              maxWidth={"90%"}
            >
              <LanguageSwitcher />
              <Button onClick={handleClick} variant={"ghost"}>
                <FiMenu size={width > 960 ? 20 : 25} />
              </Button>
            </Container>
          </NavbarList>
        </NavbarInnerContainer>
        {contents[categoryShown]}
        <DropdownMenu
          display={menu ? "block" : "none"}
          handleClick={handleClick}
          setStatus={setMenuStatus}
          status={menuStatus}
        />
      </NavbarContainer>
    );
  } else if (screen === "medium") {
    return (
      <NavbarContainer id={"navbar"} ref={menuRef}>
        {isSecondaryMenuVisible ? (
          <Container
            align={"center"}
            bgColor={"#f4f4f6"}
            display={"flex"}
            height={"50px"}
            justify={"center"}
          >
            <Container display={"flex"} justify={"end"} maxWidth={"1222px"}>
              <AirsLink
                decoration={"none"}
                href={"https://app.fluidattacks.com/"}
              >
                <LoginButton>
                  <BsFillPersonFill />
                  {translate.t("menu.buttons.login")}
                </LoginButton>
              </AirsLink>
              <LanguageSwitcher />
            </Container>
          </Container>
        ) : undefined}
        <NavbarInnerContainer id={"inner_navbar"}>
          <NavbarList className={"poppins"} id={"navbar_list"}>
            <div className={"w-auto flex flex-nowrap"}>
              <li>
                <Link className={"db tc pa1 no-underline"} to={"/"}>
                  <Container display={"block"} ph={3} pv={2} width={"160px"}>
                    <CloudImage
                      alt={"Fluid Attacks logo navbar"}
                      src={"airs/menu/Logo.png"}
                    />
                  </Container>
                </Link>
              </li>
            </div>
            <Container
              display={"flex"}
              justify={"end"}
              minWidth={"447px"}
              width={"80%"}
              wrap={"nowrap"}
            >
              <AirsLink href={"/contact-us/"}>
                <Button variant={"tertiary"}>{"Contact now"}</Button>
              </AirsLink>
              <Container maxWidth={"142px"} ml={2} mr={2}>
                <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                  <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                    {"Try for free"}
                  </Button>
                </AirsLink>
              </Container>
            </Container>
            <Container
              display={"flex"}
              justify={"center"}
              justifyMd={"end"}
              justifySm={"end"}
              maxWidth={"50px"}
            >
              <Button onClick={handleClick} variant={"ghost"}>
                <FiMenu size={width > 960 ? 20 : 25} />
              </Button>
            </Container>
          </NavbarList>
        </NavbarInnerContainer>
        {contents[categoryShown]}
        <DropdownMenu
          display={menu ? "block" : "none"}
          handleClick={handleClick}
          setStatus={setMenuStatus}
          status={menuStatus}
        />
      </NavbarContainer>
    );
  }

  return (
    <NavbarContainer id={"navbar"} ref={menuRef}>
      {isSecondaryMenuVisible ? (
        <Container
          align={"center"}
          bgColor={"#f4f4f6"}
          display={"flex"}
          height={"50px"}
          justify={"center"}
        >
          <Container display={"flex"} justify={"end"} maxWidth={"1154px"}>
            <AirsLink
              decoration={"none"}
              href={"https://app.fluidattacks.com/"}
            >
              <LoginButton>
                <BsFillPersonFill />
                {translate.t("menu.buttons.login")}
              </LoginButton>
            </AirsLink>
            <LanguageSwitcher />
          </Container>
        </Container>
      ) : undefined}

      <NavbarInnerContainer id={"inner_navbar"}>
        <NavbarList className={"poppins"} id={"navbar_list"}>
          <div className={"w-auto flex flex-nowrap"}>
            <li>
              <Link
                className={"db tc pa1 no-underline"}
                to={i18next.language === "es" ? "/es/" : "/"}
              >
                <Container display={"block"} ph={3} pv={2} width={"160px"}>
                  <CloudImage
                    alt={"Fluid Attacks logo navbar"}
                    src={"airs/menu/Logo.png"}
                  />
                </Container>
              </Link>
            </li>
          </div>
          <Container center={true} display={"flex"} width={"auto"}>
            <Button
              customSize={customOptionsButtonSize}
              icon={<Chevron direction={chevrons.services} />}
              iconSide={"right"}
              onClick={handleClickButton("services")}
              variant={"ghost"}
            >
              {translate.t("menu.buttons.service")}
            </Button>
            <Button
              customSize={customOptionsButtonSize}
              icon={<Chevron direction={chevrons.platform} />}
              iconSide={"right"}
              onClick={handleClickButton("platform")}
              variant={"ghost"}
            >
              {translate.t("menu.buttons.platform")}
            </Button>
            <AirsLink href={"/plans/"}>
              <Button customSize={customOptionsButtonSize} variant={"ghost"}>
                {translate.t("menu.buttons.plans")}
              </Button>
            </AirsLink>
            <Button
              customSize={customOptionsButtonSize}
              icon={<Chevron direction={chevrons.resources} />}
              iconSide={"right"}
              onClick={handleClickButton("resources")}
              variant={"ghost"}
            >
              {translate.t("menu.buttons.resources")}
            </Button>
            <AirsLink href={"/advisories/"}>
              <Button customSize={customOptionsButtonSize} variant={"ghost"}>
                {translate.t("menu.buttons.advisories")}
              </Button>
            </AirsLink>
            <Button
              customSize={customOptionsButtonSize}
              icon={<Chevron direction={chevrons.company} />}
              iconSide={"right"}
              onClick={handleClickButton("company")}
              variant={"ghost"}
            >
              {translate.t("menu.buttons.company")}
            </Button>
          </Container>
          <Container
            display={"flex"}
            justify={"end"}
            minWidth={"365px"}
            width={"auto"}
            wrap={"nowrap"}
          >
            <AirsLink href={"/contact-us/"}>
              <Button variant={"tertiary"}>
                {translate.t("menu.buttons.contact")}
              </Button>
            </AirsLink>
            <Container maxWidth={"200px"} ml={2} mr={2}>
              <AirsLink href={"https://app.fluidattacks.com/SignUp"}>
                <Button onClick={matomoFreeTrialEvent} variant={"primary"}>
                  {translate.t("menu.buttons.trial")}
                </Button>
              </AirsLink>
            </Container>
          </Container>
        </NavbarList>
      </NavbarInnerContainer>
      {contents[categoryShown]}
    </NavbarContainer>
  );
};
