import _ from "lodash";

import type { IRootAttr } from "../types";

const cleanCredentialsValues = (
  setFieldValue: (
    field: string,
    value: boolean | string,
    shouldValidate?: boolean | undefined
  ) => void
): void => {
  setFieldValue("credentials.name", "", false);
  setFieldValue("credentials.id", "", false);
  setFieldValue("credentials.password", "", false);
  setFieldValue("credentials.token", "", false);
  setFieldValue("credentials.user", "", false);
  setFieldValue("credentials.key", "", false);
  setFieldValue("credentials.azureOrganization", "", false);
  setFieldValue("credentials.type", "", false);
  setFieldValue("credentials.typeCredential", "", false);
};

const chooseCredentialType = (
  url: string,
  setFieldValue: (
    field: string,
    value: boolean | string,
    shouldValidate?: boolean | undefined
  ) => void
): void => {
  const httpsRegex = /^https:\/\/(?:(?!\b.*dev\.azure\.com\b)).*/u;
  const azureRegex = /.*(?:dev\.azure\.com).*/u;
  const sshRegex = /^(?:ssh|git@).*/u;
  if (azureRegex.test(url)) {
    cleanCredentialsValues(setFieldValue);
    setFieldValue("credentials.typeCredential", "TOKEN", false);
    setFieldValue("credentials.type", "HTTPS", false);
    setFieldValue("credentials.auth", "TOKEN", false);
    setFieldValue("credentials.isPat", true, false);
  }

  if (httpsRegex.test(url)) {
    cleanCredentialsValues(setFieldValue);
    setFieldValue("credentials.typeCredential", "USER", false);
    setFieldValue("credentials.type", "HTTPS", false);
    setFieldValue("credentials.auth", "USER", false);
    setFieldValue("credentials.isPat", false, false);
  }

  if (sshRegex.test(url)) {
    cleanCredentialsValues(setFieldValue);
    setFieldValue("credentials.typeCredential", "SSH", false);
    setFieldValue("credentials.type", "SSH", false);
    setFieldValue("credentials.auth", "", false);
    setFieldValue("credentials.isPat", false, false);
  }

  if (!azureRegex.test(url) && !httpsRegex.test(url) && !sshRegex.test(url)) {
    cleanCredentialsValues(setFieldValue);
  }
};

const submittableCredentials = (values: IRootAttr): boolean => {
  if (
    values.credentials.typeCredential === "SSH" &&
    (!values.credentials.name || !values.credentials.key || !values.branch)
  ) {
    return true;
  }
  if (
    values.credentials.typeCredential === "USER" &&
    (!values.credentials.name ||
      !values.credentials.user ||
      !values.credentials.password ||
      !values.branch)
  ) {
    return true;
  }
  if (
    values.credentials.typeCredential === "TOKEN" &&
    (!values.credentials.name ||
      !values.credentials.token ||
      _.isEmpty(values.credentials.azureOrganization) ||
      !values.branch)
  ) {
    return true;
  }

  return false;
};

export { chooseCredentialType, submittableCredentials };
