import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { useFormikContext } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useContext, useEffect, useMemo } from "react";
import type { ChangeEvent, FC } from "react";
import { useTranslation } from "react-i18next";

import type { ICredentialSection } from "./types";
import { getCredentials } from "./utils ";

import { GET_ORGANIZATION_CREDENTIALS } from "../../queries";
import type { ICredentialsAttr, IFormValues } from "../../types";
import { Select } from "components/Input";
import { Row } from "components/Layout";
import { groupContext } from "scenes/Dashboard/group/context";
import type { IGroupContext } from "scenes/Dashboard/group/types";
import { Logger } from "utils/logger";

const CredentialSection: FC<ICredentialSection> = ({
  trialOrgId,
  provider,
}): JSX.Element => {
  const { t } = useTranslation();
  const { setFieldValue, values } = useFormikContext<IFormValues>();

  const { organizationId }: IGroupContext = useContext(groupContext);

  const orgId = useMemo((): string => {
    if (_.isUndefined(provider) && !_.isUndefined(trialOrgId)) {
      return trialOrgId;
    }

    return organizationId;
  }, [organizationId, trialOrgId, provider]);

  const { data } = useQuery<{
    organization: { credentials: ICredentialsAttr[] };
  }>(GET_ORGANIZATION_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load organization credentials", error);
      });
    },
    variables: {
      organizationId: orgId,
    },
  });

  const credentialsData = useMemo((): ICredentialsAttr[] => {
    if (_.isUndefined(data)) {
      return [];
    }

    if (_.isUndefined(provider)) {
      return data.organization.credentials;
    }

    return getCredentials(data.organization.credentials, provider);
  }, [data, provider]);

  const credentials = useMemo((): Record<string, ICredentialsAttr> => {
    return credentialsData.length > 0
      ? Object.fromEntries(
          credentialsData.map((cred): [string, ICredentialsAttr] => [
            cred.id,
            cred,
          ])
        )
      : {};
  }, [credentialsData]);

  const onChangeCredential = useCallback(
    (event: ChangeEvent<HTMLSelectElement>): void => {
      if (!_.isEmpty(event.target.value)) {
        const currentCred = credentials[event.target.value];
        setFieldValue("credentials.type", currentCred.type);
        setFieldValue("credentials.oauthType", currentCred.oauthType);
        setFieldValue("credentials.name", currentCred.name);
        setFieldValue("credentials.isPat", currentCred.isPat);
        setFieldValue("credentials.isToken", currentCred.isToken);
      }
    },
    [credentials, setFieldValue]
  );

  useEffect((): void => {
    if (
      values.credentials.id === "" &&
      _.isUndefined(provider) &&
      !_.isUndefined(credentialsData[0])
    ) {
      setFieldValue("credentials.id", credentialsData[0].id);
      setFieldValue("credentials.name", credentialsData[0].name);
    }
  }, [credentialsData, provider, setFieldValue, values]);

  return (
    <Row>
      <Select
        label={t("components.oauthRootForm.credentialSection.label")}
        name={"credentials.id"}
        onChange={onChangeCredential}
      >
        <option value={""}>{""}</option>
        {Object.values(credentials).map(
          (cred): JSX.Element => (
            <option key={cred.id} value={cred.id}>
              {cred.name}
            </option>
          )
        )}
      </Select>
    </Row>
  );
};

export { CredentialSection };
