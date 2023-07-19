import { useQuery } from "@apollo/client";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { useRouteMatch } from "react-router-dom";

import type { IUserRole } from "./queries";
import { GET_USER_ROLE } from "./queries";
import { getLevel } from "./utils";

import { Text } from "components/Text";

const Role: React.FC = (): JSX.Element | null => {
  const { t } = useTranslation();

  const match = useRouteMatch<{ groupName: string; organizationName: string }>([
    "/orgs/:organizationName/groups/:groupName",
    "/orgs/:organizationName/groups",
  ]);
  const { groupName, organizationName } = match?.params ?? {};
  const level = getLevel(groupName, organizationName);

  const { data } = useQuery<IUserRole>(GET_USER_ROLE, {
    variables: {
      groupLevel: level === "group",
      groupName: groupName ?? "",
      organizationLevel: level === "organization",
      organizationName: organizationName ?? "",
      userLevel: level === "user",
    },
  });

  if (data === undefined) {
    return null;
  }

  const role = {
    group: data.group?.userRole,
    organization: data.organizationId?.userRole,
    user: data.me?.role,
  }[level];

  return (
    <Text bright={7} mb={1}>
      {t("navbar.role")}
      &nbsp;
      {t(`userModal.roles.${_.camelCase(role)}`)}
    </Text>
  );
};

export { Role };
