import React from "react";
import { Redirect, Route, Switch } from "react-router-dom";

import { useInitialOrganization, useStartUrl } from "./hooks";
import { LegalNotice } from "./legal-notice";
import { useLegalNotice } from "./legal-notice/hooks";
import { Navbar } from "./navbar";
import { OrganizationRedirect } from "./organization-redirect";
import { SessionIdle } from "./session-idle";
import { Sidebar } from "./sidebar";
import { DashboardContainer, DashboardContent } from "./styles";
import { TrialTimeBanner } from "./trial-time-banner";

import { ScrollUpButton } from "components/ScrollUpButton";
import { Group } from "pages/group";
import { Organization } from "pages/organization";
import { Portfolio } from "pages/portfolio";
import { ToDo } from "pages/to-do";
import { User } from "pages/user";

/*
 * Main application paths
 * {@link https://v5.reactrouter.com/web/api/Route/path-string-string}
 */
const ORGANIZATION_PATH = "/orgs/:organizationName([a-zA-Z0-9]+)";
const GROUP_PATH = `${ORGANIZATION_PATH}/groups/:groupName([a-zA-Z0-9]+)`;
const PORTFOLIO_PATH = `${ORGANIZATION_PATH}/portfolios/:tagName([a-zA-Z0-9-_ ]+)`;
const TODO_PATH = "/todos";
const USER_PATH = "/user";

// Legacy paths kept for backwards-compatibility
const LEGACY_GROUP_PATH = "/groups/:groupName([a-zA-Z0-9]+)";
const LEGACY_PORTFOLIO_PATH = "/portfolios/:tagName([a-zA-Z0-9-_ ]+)";

const Dashboard: React.FC = (): JSX.Element => {
  const initialOrganization = useInitialOrganization();
  const { acceptLegalNotice, legalNoticeOpen } = useLegalNotice();
  useStartUrl();

  if (initialOrganization === undefined || legalNoticeOpen === undefined) {
    return <div />;
  }

  if (legalNoticeOpen) {
    return <LegalNotice onAccept={acceptLegalNotice} />;
  }

  return (
    <DashboardContainer>
      <Route path={ORGANIZATION_PATH}>
        <TrialTimeBanner />
      </Route>
      <Navbar />
      <div className={"flex flex-auto flex-row"}>
        <Sidebar />
        <DashboardContent id={"dashboard"}>
          <Switch>
            <Route path={GROUP_PATH}>
              <Group />
            </Route>
            <Route path={PORTFOLIO_PATH}>
              <Portfolio />
            </Route>
            <Route path={ORGANIZATION_PATH}>
              <Organization />
            </Route>
            <Route path={TODO_PATH}>
              <ToDo />
            </Route>
            <Route path={USER_PATH}>
              <User />
            </Route>
            <Route path={LEGACY_GROUP_PATH}>
              <OrganizationRedirect type={"group"} />
            </Route>
            <Route path={LEGACY_PORTFOLIO_PATH}>
              <OrganizationRedirect type={"portfolio"} />
            </Route>
            {/* Fallback if none of the paths were matched */}
            <Redirect to={`/orgs/${initialOrganization}`} />
          </Switch>
          <ScrollUpButton />
          <SessionIdle />
        </DashboardContent>
      </div>
    </DashboardContainer>
  );
};

export { Dashboard };
