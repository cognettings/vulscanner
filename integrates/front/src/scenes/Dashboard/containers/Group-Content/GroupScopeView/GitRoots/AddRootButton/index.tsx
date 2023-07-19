import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useContext } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { GET_ORGANIZATION_CREDENTIALS } from "./queries";
import type { IAddRootProps, ICredentialsAttr } from "./types";
import { showProviders } from "./utils";

import { RepositoriesDropdown } from "scenes/Dashboard/components/RepositoriesDropdown";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";
import { Logger } from "utils/logger";

const AddRootButton: FC<IAddRootProps> = ({
  manualClick,
  providersClick,
}): JSX.Element => {
  const { t } = useTranslation();
  const { organizationId }: IGroupContext = useContext(groupContext);

  const { push } = useHistory();
  const { organizationName } = useParams<{ organizationName: string }>();

  const onMoveToCredentials = useCallback((): void => {
    push(`/orgs/${organizationName}/credentials`);
  }, [organizationName, push]);

  const { data } = useQuery<{
    organization: { credentials: ICredentialsAttr[] };
  }>(GET_ORGANIZATION_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load organization credentials", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  const credentials: ICredentialsAttr[] = _.isUndefined(data)
    ? []
    : data.organization.credentials;

  const availableProviders = showProviders(credentials);

  const azureClick = useCallback((): void => {
    providersClick("AZURE");
  }, [providersClick]);

  const bitbucketClick = useCallback((): void => {
    providersClick("BITBUCKET");
  }, [providersClick]);

  const gitHubClick = useCallback((): void => {
    providersClick("GITHUB");
  }, [providersClick]);

  const gitLabClick = useCallback((): void => {
    providersClick("GITLAB");
  }, [providersClick]);

  const repositories = {
    azure: {
      isVisible: availableProviders.azure,
      onClick: azureClick,
    },
    bitbucket: {
      isVisible: availableProviders.bitbucket,
      onClick: bitbucketClick,
    },
    gitHub: {
      isVisible: availableProviders.gitHub,
      onClick: gitHubClick,
    },
    gitLab: {
      isVisible: availableProviders.gitLab,
      onClick: gitLabClick,
    },
    manual: {
      isVisible: true,
      onClick: manualClick,
    },
    other: {
      isVisible: true,
      onClick: onMoveToCredentials,
      text: "Other host",
    },
  };

  return (
    <RepositoriesDropdown
      availableRepositories={repositories}
      dropDownText={t("group.scope.common.add")}
    />
  );
};

export { AddRootButton };
