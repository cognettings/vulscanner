import { navigate } from "gatsby";
import i18next, { changeLanguage } from "i18next";
import React, { useCallback, useState } from "react";
import { FiChevronDown } from "react-icons/fi";
import { IoIosGlobe } from "react-icons/io";

import {
  LanguagesButton,
  LanguagesContainer,
  Switcher,
} from "./StyledComponents";

import { Container } from "../../../../components/Container";
import { useWindowLocation } from "../../../../utils/hooks/useWindowLocation";
import { translatedPages } from "../../../../utils/translations/spanishPages";

export const LanguageSwitcher: React.FC = (): JSX.Element => {
  const [displayLanguages, setDisplayLanguages] = useState(false);
  const handleClickButton = useCallback(
    (): (() => void) => (): void => {
      setDisplayLanguages(!displayLanguages);
    },
    [displayLanguages]
  );
  const location = useWindowLocation();
  const newLocation = `/${location}`;
  const spanishHref = translatedPages.find(
    (page): boolean => page.en === newLocation
  );
  const englishHref = translatedPages.find(
    (page): boolean => page.es === newLocation
  );

  const updateLanguage = async (newLanguage: string): Promise<void> => {
    await changeLanguage(newLanguage);
  };

  const navigateToPage = async (pagePath: string): Promise<void> => {
    await navigate(pagePath, { replace: true });
  };

  const locationEs = spanishHref ? (spanishHref.es ? spanishHref.es : "") : "";
  const locationEn = englishHref ? (englishHref.en ? englishHref.en : "") : "";
  const languageHandler = useCallback(
    (language: string): (() => void) =>
      (): void => {
        if (language === "es" && locationEs !== "") {
          void navigateToPage(locationEs);
          void updateLanguage("es");
        } else if (language === "en" && locationEn !== "") {
          void navigateToPage(locationEn);
          void updateLanguage("en");
        }
      },
    [locationEn, locationEs]
  );
  if (useWindowLocation().startsWith("es/")) {
    void updateLanguage("es");
  }

  return (
    <Container
      display={"flex"}
      maxWidth={"122px"}
      position={"relative"}
      wrap={"wrap"}
    >
      <Switcher onClick={handleClickButton()}>
        <IoIosGlobe size={15} />
        {i18next.language === "en" ? "English" : "Español"}
        <FiChevronDown />
      </Switcher>
      <LanguagesContainer isShown={displayLanguages}>
        <LanguagesButton
          disabled={i18next.language === "en"}
          onClick={languageHandler("en")}
        >
          {"English"}
        </LanguagesButton>
        <LanguagesButton
          disabled={i18next.language === "es"}
          onClick={languageHandler("es")}
        >
          {"Español"}
        </LanguagesButton>
      </LanguagesContainer>
    </Container>
  );
};
