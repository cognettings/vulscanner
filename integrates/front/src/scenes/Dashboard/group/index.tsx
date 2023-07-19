import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, {
  StrictMode,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
import { useTranslation } from "react-i18next";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import { groupContext, vulnerabilitiesContext } from "./context";
import { GET_GROUP_EVENT_STATUS } from "./queries";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { Dot } from "components/Dot";
import { Lottie } from "components/Icon";
import { useShow } from "components/Modal";
import { Tab, TabContent, Tabs } from "components/Tabs";
import { Text } from "components/Text";
import { Can } from "context/authz/Can";
import { authzPermissionsContext } from "context/authz/config";
import { Have } from "context/authz/Have";
import { featurePreviewContext } from "context/featurePreview";
import { useTabTracking } from "hooks";
import { HelpModal } from "pages/home/dashboard/navbar/help-modal";
import { lotCircleXMark } from "resources";
import { EventBar } from "scenes/Dashboard/components/EventBar";
import { ChartsForGroupView } from "scenes/Dashboard/containers/Group-Content/ChartsForGroupView";
import { GroupAuthorsView } from "scenes/Dashboard/containers/Group-Content/GroupAuthorsView";
import { GroupConsultingView } from "scenes/Dashboard/containers/Group-Content/GroupConsultingView/index";
import { GroupEventsView } from "scenes/Dashboard/containers/Group-Content/GroupEventsView/index";
import { GroupFindingsView } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/index";
import { GroupForcesView } from "scenes/Dashboard/containers/Group-Content/GroupForcesView";
import { GroupInternalContent } from "scenes/Dashboard/containers/Group-Content/GroupInternalContent";
import { GroupScopeView } from "scenes/Dashboard/containers/Group-Content/GroupScopeView";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/queries";
import type { IGroupData } from "scenes/Dashboard/containers/Group-Content/GroupScopeView/GroupSettingsView/Services/types";
import { GroupStakeholdersView } from "scenes/Dashboard/containers/Group-Content/GroupStakeholdersView/index";
import { GroupVulnerabilitiesView } from "scenes/Dashboard/containers/Group-Content/GroupVulnerabilitiesView";
import { ToeContent } from "scenes/Dashboard/containers/Group-Content/ToeContent";
import { GET_ORGANIZATION_ID } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/queries";
import type { IGetOrganizationId } from "scenes/Dashboard/containers/Organization-Content/OrganizationNav/types";
import type {
  IGetEventStatus,
  IGroupContext,
  IVulnerabilitiesContext,
} from "scenes/Dashboard/group/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const GroupContent: React.FC = (): JSX.Element => {
  const { path, url } = useRouteMatch<{ path: string; url: string }>();
  const { groupName, organizationName } =
    useParams<{ groupName: string; organizationName: string }>();
  const { featurePreview } = useContext(featurePreviewContext);
  const [denyAccess, setDenyAccess] = useState(false);
  const [openVulnerabilities, setOpenVulnerabilities] = useState<number>(0);
  const [show, open, close] = useShow();
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canGetToeLines: boolean = permissions.can(
    "api_resolvers_group_toe_lines_connection_resolve"
  );
  const canGetToeInputs: boolean = permissions.can(
    "api_resolvers_group_toe_inputs_resolve"
  );

  const continueAccess = useCallback((): void => {
    setDenyAccess(false);
  }, [setDenyAccess]);

  // GraphQL Operations
  const { data: orgData } = useQuery<IGetOrganizationId>(GET_ORGANIZATION_ID, {
    fetchPolicy: "cache-first",
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching organization ID", error);
      });
    },
    variables: {
      organizationName: organizationName.toLowerCase(),
    },
  });
  void useQuery<IGroupData>(GET_GROUP_DATA, {
    onCompleted: ({ group: { managed } }): void => {
      setDenyAccess(managed === "UNDER_REVIEW");
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName },
  });
  const { data } = useQuery<IGetEventStatus>(GET_GROUP_EVENT_STATUS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.warning("An error occurred loading event bar data", error);
        msgError(t("groupAlerts.errorTextsad"));
      });
    },
    variables: { groupName },
  });

  const hasOpenEvents = useMemo(
    (): boolean =>
      data === undefined
        ? false
        : data.group.events.some(
            (event): boolean => event.eventStatus === "CREATED"
          ),
    [data]
  );

  const vulnValue = useMemo(
    (): IVulnerabilitiesContext => ({
      openVulnerabilities,
      setOpenVulnerabilities,
    }),
    [openVulnerabilities]
  );
  const tip = useMemo(
    (): string =>
      openVulnerabilities === 0
        ? t("group.tabs.findings.tooltip.default")
        : t("group.tabs.findings.tooltip.openVulns", {
            value: openVulnerabilities,
          }),
    [openVulnerabilities, t]
  );

  const organizationId = useMemo(
    (): string => (_.isUndefined(orgData) ? "" : orgData.organizationId.id),
    [orgData]
  );

  const value = useMemo(
    (): IGroupContext => ({ organizationId, path, url }),
    [organizationId, path, url]
  );

  // Side effects
  useTabTracking("Group");

  if (_.isUndefined(orgData)) {
    return <div />;
  }

  return (
    <StrictMode>
      {denyAccess ? (
        <div className={"flex justify-center mt5"}>
          <Card>
            <div className={"flex justify-center mb3 mt3"}>
              <Lottie animationData={lotCircleXMark} size={100} />
            </div>
            <Text fw={7} mb={3} size={"medium"} ta={"center"}>
              {t("group.accessDenied.title")}
            </Text>
            <Text mb={3} ta={"center"}>
              {t("group.accessDenied.text")}
              <Button onClick={open} size={"xs"}>
                <Text decor={["under"]}>{t("group.accessDenied.contact")}</Text>
              </Button>
              {t("group.accessDenied.moreInfo")}
            </Text>
            <Can I={"api_mutations_update_group_managed_mutate"}>
              <div className={"flex justify-center"}>
                <Button onClick={continueAccess} variant={"primary"}>
                  {t("group.accessDenied.btn")}
                </Button>
              </div>
            </Can>
          </Card>
          <HelpModal onClose={close} open={show} />
        </div>
      ) : (
        <React.StrictMode>
          <EventBar organizationName={organizationName} />
          <Tabs>
            <Tab id={"findingsTab"} link={`${url}/vulns`} tooltip={tip}>
              {t("group.tabs.findings.text")}
            </Tab>
            <Tab
              id={"analyticsTab"}
              link={`${url}/analytics`}
              tooltip={t("group.tabs.indicators.tooltip")}
            >
              {t("group.tabs.analytics.text")}
            </Tab>
            <Tab
              id={"forcesTab"}
              link={`${url}/devsecops`}
              tooltip={t("group.tabs.forces.tooltip")}
            >
              {t("group.tabs.forces.text")}
            </Tab>
            <Tab
              id={"eventsTab"}
              link={`${url}/events`}
              tooltip={t("group.tabs.events.tooltip")}
            >
              {t("group.tabs.events.text")}
              {hasOpenEvents ? <Dot /> : undefined}
            </Tab>
            <Have I={"has_squad"}>
              <Can do={"api_resolvers_group_consulting_resolve"}>
                <Tab
                  id={"commentsTab"}
                  link={`${url}/consulting`}
                  tooltip={t("group.tabs.comments.tooltip")}
                >
                  {t("group.tabs.comments.text")}
                </Tab>
              </Can>
            </Have>
            <Can do={"api_resolvers_query_stakeholder__resolve_for_group"}>
              <Tab
                id={"usersTab"}
                link={`${url}/members`}
                tooltip={t("group.tabs.users.tooltip")}
              >
                {t("group.tabs.users.text")}
              </Tab>
            </Can>
            <Have I={"has_service_white"}>
              <Can do={"api_resolvers_group_billing_resolve"}>
                <Tab
                  id={"authorsTab"}
                  link={`${url}/authors`}
                  tooltip={t("group.tabs.authors.tooltip")}
                >
                  {t("group.tabs.authors.text")}
                </Tab>
              </Can>
            </Have>
            {!canGetToeInputs && !canGetToeLines ? undefined : (
              <Tab
                id={"toeTab"}
                link={`${url}/surface`}
                tooltip={t("group.tabs.toe.tooltip")}
              >
                {t("group.tabs.toe.text")}
              </Tab>
            )}
            <Tab
              id={"resourcesTab"}
              link={`${url}/scope`}
              tooltip={t("group.tabs.resources.tooltip")}
            >
              {t("group.tabs.resources.text")}
            </Tab>
          </Tabs>
          <TabContent>
            <groupContext.Provider value={value}>
              <vulnerabilitiesContext.Provider value={vulnValue}>
                <Switch>
                  <Route
                    component={GroupAuthorsView}
                    exact={true}
                    path={`${path}/authors`}
                  />
                  <Route
                    component={ChartsForGroupView}
                    exact={true}
                    path={`${path}/analytics`}
                  />
                  <Route
                    component={
                      featurePreview
                        ? GroupVulnerabilitiesView
                        : GroupFindingsView
                    }
                    path={`${path}/vulns`}
                  />
                  <Route
                    component={GroupForcesView}
                    exact={true}
                    path={`${path}/devsecops`}
                  />
                  <Route
                    component={GroupEventsView}
                    exact={true}
                    path={`${path}/events`}
                  />
                  <Route
                    component={GroupScopeView}
                    exact={true}
                    path={`${path}/scope`}
                  />
                  <Route
                    component={GroupStakeholdersView}
                    exact={true}
                    path={`${path}/members`}
                  />
                  <Route
                    component={GroupConsultingView}
                    exact={true}
                    path={`${path}/consulting`}
                  />
                  <Route component={ToeContent} path={`${path}/surface`} />
                  <Route
                    component={GroupInternalContent}
                    path={`${path}/internal`}
                  />
                  <Redirect
                    from={`${path}/stakeholders`}
                    to={`${path}/members`}
                  />
                  <Redirect to={`${path}/vulns`} />
                </Switch>
              </vulnerabilitiesContext.Provider>
            </groupContext.Provider>
          </TabContent>
        </React.StrictMode>
      )}
    </StrictMode>
  );
};

export { GroupContent };
