import { faHome } from "@fortawesome/free-solid-svg-icons";
import React, { useContext } from "react";
import { Link, Route, Switch } from "react-router-dom";

import { OrganizationTabs } from "./organization-tabs";
import { SidebarContainer, SidebarMenu } from "./styles";

import { Logo } from "components/Logo";
import { SideBar, SideBarTab } from "components/SideBar";
import {
  authzPermissionsContext,
  organizationLevelPermissions,
} from "context/authz/config";
import { featurePreviewContext } from "context/featurePreview";

const Sidebar: React.FC = (): JSX.Element => {
  const { featurePreview } = useContext(featurePreviewContext);

  if (featurePreview) {
    return (
      <Switch>
        <authzPermissionsContext.Provider value={organizationLevelPermissions}>
          <SideBar>
            <SideBarTab icon={faHome} to={"/home"} />
            <Route path={"/orgs/:org/"}>
              <OrganizationTabs />
            </Route>
          </SideBar>
        </authzPermissionsContext.Provider>
      </Switch>
    );
  }

  return (
    <SidebarContainer>
      <SidebarMenu>
        <li>
          <Link to={"/home"}>
            <Logo height={45} width={45} />
          </Link>
        </li>
      </SidebarMenu>
    </SidebarContainer>
  );
};

export { Sidebar };
