import React from "react";

import { Hero } from "../../../components/Hero";
import { translate } from "../../../utils/translations/translate";

const HeaderHero: React.FC = (): JSX.Element => {
  return (
    <Hero
      button1Link={"https://app.fluidattacks.com/SignUp"}
      button1Text={translate.t("home.hero.button1")}
      button2Link={"/contact-us/"}
      button2Text={translate.t("home.hero.button2")}
      image={"airs/home/HeaderHero/hero-image"}
      matomoAction={"Home"}
      paragraph={translate.t("home.hero.paragraph")}
      size={"big"}
      sizeSm={"medium"}
      title={translate.t("home.hero.title")}
      tone={"dark"}
      variant={"right"}
    />
  );
};

export { HeaderHero };
