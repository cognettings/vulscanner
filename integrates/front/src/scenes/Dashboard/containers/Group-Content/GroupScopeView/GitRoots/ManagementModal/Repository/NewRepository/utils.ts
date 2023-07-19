import type { FormikProps } from "formik";
import _ from "lodash";
import type { Dispatch, SetStateAction } from "react";

import type { IFormValues } from "../../../../types";
import { formatBooleanHealthCheck } from "../../../../utils";
import { translate } from "utils/translations/translate";

const cleanCredentialsValues = (
  setCredExists: React.Dispatch<React.SetStateAction<boolean>>,
  setFieldValue: (
    field: string,
    value: boolean | string,
    shouldValidate?: boolean | undefined
  ) => void
): void => {
  setCredExists(false);
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
  isCredExisting: boolean,
  setCredExists: React.Dispatch<React.SetStateAction<boolean>>,
  setFieldValue: (
    field: string,
    value: boolean | string,
    shouldValidate?: boolean | undefined
  ) => void
): void => {
  const httpsRegex = /^https:\/\/(?:(?!\b.*dev\.azure\.com\b)).*/u;
  const azureRegex = /.*(?:dev\.azure\.com).*/u;
  const sshRegex = /^(?:ssh|git@).*/u;
  if (!isCredExisting) {
    if (azureRegex.test(url)) {
      cleanCredentialsValues(setCredExists, setFieldValue);
      setFieldValue("credentials.typeCredential", "TOKEN", false);
      setFieldValue("credentials.type", "HTTPS", false);
      setFieldValue("credentials.auth", "TOKEN", false);
      setFieldValue("credentials.isPat", true, false);
    }

    if (httpsRegex.test(url)) {
      cleanCredentialsValues(setCredExists, setFieldValue);
      setFieldValue("credentials.typeCredential", "USER", false);
      setFieldValue("credentials.type", "HTTPS", false);
      setFieldValue("credentials.auth", "USER", false);
      setFieldValue("credentials.isPat", false, false);
    }

    if (sshRegex.test(url)) {
      cleanCredentialsValues(setCredExists, setFieldValue);
      setFieldValue("credentials.typeCredential", "SSH", false);
      setFieldValue("credentials.type", "SSH", false);
      setFieldValue("credentials.auth", "", false);
      setFieldValue("credentials.isPat", false, false);
    }
    if (!azureRegex.test(url) && !httpsRegex.test(url) && !sshRegex.test(url)) {
      cleanCredentialsValues(setCredExists, setFieldValue);
    }
  }

  if (
    isCredExisting &&
    ((!azureRegex.test(url) && !httpsRegex.test(url) && !sshRegex.test(url)) ||
      url === "")
  ) {
    cleanCredentialsValues(setCredExists, setFieldValue);
  }
};

const hasSshFormat = (value: string): string | undefined => {
  const regex =
    /^-{5}BEGIN OPENSSH PRIVATE KEY-{5}\n(?:[a-zA-Z0-9+/=]+\n)+-{5}END OPENSSH PRIVATE KEY-{5}\n?$/u;

  if (!regex.test(value)) {
    return translate.t("validations.invalidSshFormat");
  }

  return undefined;
};

const submittableCredentials = (
  credExists: boolean,
  values: IFormValues
): boolean => {
  if (values.useVpn || credExists) {
    return true;
  }
  if (values.credentials.typeCredential === "") {
    return true;
  }
  if (
    values.credentials.typeCredential === "SSH" &&
    (!values.credentials.name ||
      !values.credentials.key ||
      hasSshFormat(values.credentials.key) !== undefined)
  ) {
    return true;
  }
  if (
    values.credentials.typeCredential === "USER" &&
    (!values.credentials.name ||
      !values.credentials.user ||
      !values.credentials.password)
  ) {
    return true;
  }
  if (
    values.credentials.typeCredential === "TOKEN" &&
    (!values.credentials.name ||
      !values.credentials.token ||
      !values.credentials.azureOrganization)
  ) {
    return true;
  }

  return false;
};

const updateHealthCheckConfirm = (
  form: React.RefObject<FormikProps<IFormValues>>,
  initialValues: IFormValues,
  isEditing: boolean,
  setIsSameHealthCheck: Dispatch<SetStateAction<boolean>>,
  url?: string,
  branch?: string,
  includesHealthCheck?: boolean | string
): void => {
  if (form.current !== null) {
    const values = {
      branch: branch ?? form.current.values.branch,
      includesHealthCheck:
        includesHealthCheck ?? form.current.values.includesHealthCheck,
      url: url ?? form.current.values.url,
    };

    if (
      isEditing &&
      _.isEqual(
        [
          values.url,
          values.branch,
          formatBooleanHealthCheck(values.includesHealthCheck),
        ].join(""),
        [
          initialValues.url,
          initialValues.branch,
          initialValues.includesHealthCheck,
        ].join("")
      )
    ) {
      setIsSameHealthCheck(true);
      form.current.setFieldValue(
        "healthCheckConfirm",
        initialValues.healthCheckConfirm
      );
    } else {
      setIsSameHealthCheck(false);
      form.current.setFieldValue("healthCheckConfirm", []);
    }
  }
};

export {
  chooseCredentialType,
  submittableCredentials,
  updateHealthCheckConfirm,
};
