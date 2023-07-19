import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useContext, useEffect } from "react";
import { useTranslation } from "react-i18next";
import {
  Redirect,
  Route,
  Switch,
  useParams,
  useRouteMatch,
} from "react-router-dom";

import {
  authzGroupContext,
  authzPermissionsContext,
} from "context/authz/config";
import { FindingContent } from "scenes/Dashboard/containers/Finding-Content";
import { EventContent } from "scenes/Dashboard/containers/Group-Content/GroupRoute/EventContent";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/Group-Content/GroupRoute/queries";
import type { IGroupData } from "scenes/Dashboard/containers/Group-Content/GroupRoute/types";
import { GroupContent } from "scenes/Dashboard/group";
import { GET_GROUP_LEVEL_PERMISSIONS } from "scenes/Dashboard/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const GroupRoute: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { organizationName, groupName } = useParams<{
    organizationName: string;
    groupName: string;
  }>();
  const { path } = useRouteMatch();

  const attributes: PureAbility<string> = useContext(authzGroupContext);
  const permissions: PureAbility<string> = useContext(authzPermissionsContext);

  // Side effects
  const onGroupChange: () => void = (): void => {
    attributes.update([]);
    permissions.update([]);
  };
  useEffect(onGroupChange, [attributes, permissions, groupName]);

  // GraphQL operations
  useQuery(GET_GROUP_LEVEL_PERMISSIONS, {
    onCompleted: (permData: { group: { permissions: string[] } }): void => {
      permissions.update(
        permData.group.permissions.map(
          (
            action: string
          ): {
            action: string;
          } => ({
            action,
          })
        )
      );
      if (permData.group.permissions.length === 0) {
        Logger.error(
          "Empty permissions",
          JSON.stringify(permData.group.permissions)
        );
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((permissionsError: GraphQLError): void => {
        Logger.error("Couldn't load group-level permissions", permissionsError);
      });
    },
    variables: {
      identifier: groupName.toLowerCase(),
    },
  });

  const { data, error } = useQuery<IGroupData>(GET_GROUP_DATA, {
    onCompleted: ({ group }: IGroupData): void => {
      attributes.update(
        group.serviceAttributes.map(
          (
            attribute: string
          ): {
            action: string;
          } => ({
            action: attribute,
          })
        )
      );
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((groupError: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred group data", groupError);
      });
    },
    variables: { groupName },
  });

  if (!_.isUndefined(error)) {
    return <Redirect path={path} to={"/home"} />;
  }
  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  if (organizationName !== data.group.organization) {
    return <Redirect path={path} to={"/home"} />;
  }

  return (
    <React.StrictMode>
      <div>
        <Switch>
          <Route
            component={EventContent}
            path={`${path}/events/:eventId(\\d+)`}
          />
          <Route
            component={FindingContent}
            path={`${path}/:type(vulns|drafts)/:findingId([0-9A-Za-z]{8}-[0-9A-Za-z]{4}-4[0-9A-Za-z]{3}-[89ABab][0-9A-Za-z]{3}-[0-9A-Za-z]{12}|\\d+)`}
          />
          <Route component={GroupContent} path={path} />
        </Switch>
      </div>
    </React.StrictMode>
  );
};

export { GroupRoute };
