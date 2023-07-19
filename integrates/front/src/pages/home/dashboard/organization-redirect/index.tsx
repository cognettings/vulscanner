import { useQuery } from "@apollo/client";
import React from "react";
import { Redirect, useRouteMatch } from "react-router-dom";

import type { IGroupOrganization, IPortfolioOrganization } from "./queries";
import { GET_GROUP_ORGANIZATION, GET_PORTFOLIO_ORGANIZATION } from "./queries";

interface IOrganizationRedirectProps {
  type: "group" | "portfolio";
}

/**
 * In the past, paths did not include organization names in them.
 * This component queries the organization name and redirects accordingly.
 */
const OrganizationRedirect: React.FC<IOrganizationRedirectProps> = ({
  type,
}): JSX.Element => {
  const match = useRouteMatch<{ groupName: string; tagName: string }>();

  const { data: groupData } = useQuery<IGroupOrganization>(
    GET_GROUP_ORGANIZATION,
    {
      skip: type !== "group",
      variables: { groupName: match.params.groupName },
    }
  );
  const { data: portfolioData } = useQuery<IPortfolioOrganization>(
    GET_PORTFOLIO_ORGANIZATION,
    {
      skip: type !== "portfolio",
      variables: { tagName: match.params.tagName },
    }
  );

  if (type === "group" && groupData) {
    const { organization } = groupData.group;

    return <Redirect to={`/orgs/${organization}${match.url}`} />;
  }

  if (type === "portfolio" && portfolioData) {
    const { organization } = portfolioData.tag;

    return <Redirect to={`/orgs/${organization}${match.url}`} />;
  }

  return <div />;
};

export { OrganizationRedirect };
