import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import type { FC } from "react";

import { GET_CURRENT_USER } from "./queries";
import type { ICurrentUser } from "./types";

import { Autoenrollment } from "../auto-enrollment";
import { Dashboard } from "../dashboard";
import { GET_ROOTS } from "../queries";
import type { IRoot } from "../types";
import { Logger } from "utils/logger";

const AddRoot: FC = (): JSX.Element => {
  const [groupName, setGroupName] = useState("");

  const { data: rootsData, loading } = useQuery<{
    group: { roots: IRoot[] };
  }>(GET_ROOTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    skip: _.isEmpty(groupName),
    variables: { groupName },
  });

  const { data: userData } = useQuery<ICurrentUser>(GET_CURRENT_USER, {
    onCompleted: (data): void => {
      setGroupName(data.me.organizations[0]?.groups[0]?.name);
    },
    onError: (error): void => {
      error.graphQLErrors.forEach(({ message }): void => {
        Logger.error("Couldn't load current user", message);
      });
    },
  });

  const orgId = userData?.me.organizations[0]?.id;
  const orgName = userData?.me.organizations[0]?.name;

  const roots: IRoot[] = rootsData === undefined ? [] : rootsData.group.roots;

  if (roots.length === 0 && !loading) {
    return (
      <Autoenrollment
        initialPage={"oauthRepoForm"}
        trialGroupName={groupName}
        trialOrgId={orgId}
        trialOrgName={orgName}
      />
    );
  }

  return <Dashboard />;
};

export { AddRoot };
