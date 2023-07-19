import React from "react";
import { useTranslation } from "react-i18next";
import { Redirect, Route, Switch, useRouteMatch } from "react-router-dom";

import { EventsTaskView } from "./Events";
import { FindingEvidenceDrafts } from "./FindingEvidenceDrafts";
import { VulnerabilityDrafts } from "./VulnerabilityDrafts";

import { Tab, TabContent, Tabs } from "components/Tabs";
import { Can } from "context/authz/Can";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "context/authz/config";
import { TasksReattacks } from "scenes/Dashboard/containers/Tasks-Content/Reattacks";
import { TasksVulnerabilities } from "scenes/Dashboard/containers/Tasks-Content/Vulnerabilities";

export const TasksContent: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { path, url } = useRouteMatch<{ path: string; url: string }>();

  return (
    <React.StrictMode>
      <p className={"f3 fw7 mt4 mb3"}>{t("todoList.title")}</p>
      <Tabs>
        <Tab
          id={"assignedLocations"}
          link={`${url}/assigned-locations`}
          tooltip={t("todoList.tooltip.assignedLocations")}
        >
          {t("todoList.tabs.assignedLocations")}
        </Tab>
        <authzPermissionsContext.Provider value={userLevelPermissions}>
          <Can do={"front_can_retrieve_todo_reattacks"}>
            <Tab
              id={"tasksReattacks"}
              link={`${url}/reattacks`}
              tooltip={t("todoList.tooltip.reattacks")}
            >
              {t("todoList.tabs.reattacks")}
            </Tab>
          </Can>
          <Can do={"front_can_retrieve_todo_locations_drafts"}>
            <Tab
              id={"locationDrafts"}
              link={`${url}/location-drafts`}
              tooltip={t("todoList.tooltip.locationDrafts")}
            >
              {t("todoList.tabs.locationDrafts")}
            </Tab>
          </Can>
          <Can do={"api_mutations_approve_evidence_mutate"}>
            <Tab id={"evidenceDrafts"} link={`${url}/evidence-drafts`}>
              {t("todoList.tabs.evidenceDrafts")}
            </Tab>
          </Can>
          <Can do={"front_can_retrieve_todo_events"}>
            <Tab
              id={"tasksEvents"}
              link={`${url}/events`}
              tooltip={t("todoList.tooltip.events")}
            >
              {t("Events")}
            </Tab>
          </Can>
        </authzPermissionsContext.Provider>
      </Tabs>
      <TabContent>
        <Switch>
          <Route path={`${path}/assigned-locations/:vulnerabilityId?`}>
            <TasksVulnerabilities />
          </Route>
          <Route path={`${path}/location-drafts/:vulnerabilityId?`}>
            <VulnerabilityDrafts />
          </Route>
          <Route path={`${path}/evidence-drafts`}>
            <FindingEvidenceDrafts />
          </Route>
          <Route path={`${path}/reattacks`}>
            <TasksReattacks />
          </Route>
          <Route path={`${path}/events`}>
            <EventsTaskView />
          </Route>
          <Redirect to={`${path}/assigned-locations`} />
        </Switch>
      </TabContent>
    </React.StrictMode>
  );
};
