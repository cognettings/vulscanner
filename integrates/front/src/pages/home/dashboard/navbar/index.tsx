import React, { useContext } from "react";
import { useTranslation } from "react-i18next";

import { NavBar } from "components/NavBar";
import { Tooltip } from "components/Tooltip";
import { featurePreviewContext } from "context/featurePreview";
import { Breadcrumb } from "pages/home/dashboard/navbar/breadcrumb";
import { HelpButton } from "pages/home/dashboard/navbar/help-button";
import { NewsWidget } from "pages/home/dashboard/navbar/news-widget";
import { Searchbar } from "pages/home/dashboard/navbar/searchbar";
import { TechnicalInfo } from "pages/home/dashboard/navbar/technical-info";
import { ToDo } from "pages/home/dashboard/navbar/to-do";
import { UserProfile } from "pages/home/dashboard/navbar/user-profile";

const Navbar: React.FC = (): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);
  const { t } = useTranslation();

  return (
    <NavBar
      header={featurePreview ? undefined : <Breadcrumb />}
      variant={featurePreview ? "dark" : "light"}
    >
      <Searchbar />
      <div className={"mr2"} />
      <ToDo />
      <Tooltip id={"navbar.newsTooltip.id"} tip={t("navbar.newsTooltip")}>
        <NewsWidget />
      </Tooltip>
      <HelpButton />
      {featurePreview ? undefined : <TechnicalInfo />}
      <UserProfile />
    </NavBar>
  );
};

export { Navbar };
