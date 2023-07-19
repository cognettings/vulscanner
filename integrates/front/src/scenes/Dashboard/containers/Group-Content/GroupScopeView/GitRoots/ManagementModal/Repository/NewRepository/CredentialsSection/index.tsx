import { useFormikContext } from "formik";
import _ from "lodash";
import React, { Fragment, useCallback } from "react";
import type { ChangeEvent, FC } from "react";
import { useTranslation } from "react-i18next";

import { CredentialsType } from "./CredentialsType";
import type { ICredentialsType } from "./types";

import type { IFormValues } from "../../../../../types";
import { formatTypeCredentials } from "../../../../../utils";
import { chooseCredentialType } from "../utils";
import { Alert } from "components/Alert";
import type { IAlertProps } from "components/Alert";
import { Input, Select } from "components/Input";
import { Col } from "components/Layout";
import { Text } from "components/Text";

const CredentialsSection: FC<ICredentialsType> = ({
  credExists,
  disabledCredsEdit,
  groupedExistingCreds,
  isEditing,
  manyRows,
  repoUrl,
  setCredExists,
  setDisabledCredsEdit,
  setShowGitAlert,
  showGitAlert,
  validateGitMsg,
}): JSX.Element => {
  const { t } = useTranslation();
  const { setFieldValue, values } = useFormikContext<IFormValues>();

  const onChangeExists = useCallback(
    (event: ChangeEvent<HTMLSelectElement>): void => {
      if (event.target.value === "") {
        setCredExists(manyRows || false);
        setDisabledCredsEdit(manyRows || false);
        chooseCredentialType(repoUrl, false, setCredExists, setFieldValue);
      } else {
        const currentCred = groupedExistingCreds[event.target.value];
        setFieldValue(
          "credentials.typeCredential",
          formatTypeCredentials(currentCred)
        );
        setFieldValue("credentials.type", currentCred.type);
        setFieldValue("credentials.name", currentCred.name);
        setFieldValue("credentials.id", currentCred.id);
        setCredExists(true);
        setDisabledCredsEdit(true);
      }
    },
    [
      groupedExistingCreds,
      manyRows,
      setCredExists,
      setFieldValue,
      setDisabledCredsEdit,
      repoUrl,
    ]
  );

  const onTypeChange = useCallback(
    (event: React.ChangeEvent<HTMLSelectElement>): void => {
      event.preventDefault();
      if (event.target.value === "SSH") {
        setFieldValue("credentials.type", "SSH");
        setFieldValue("credentials.auth", "");
        setFieldValue("credentials.isPat", false);
      }
      if (event.target.value === "") {
        setFieldValue("type", "");
        setFieldValue("auth", "");
        setFieldValue("isPat", false);
      }
      if (event.target.value === "USER") {
        setFieldValue("credentials.type", "HTTPS");
        setFieldValue("credentials.auth", "USER");
        setFieldValue("credentials.isPat", false);
      }
      if (event.target.value === "TOKEN") {
        setFieldValue("credentials.type", "HTTPS");
        setFieldValue("credentials.auth", "TOKEN");
        setFieldValue("credentials.isPat", true);
      }
    },
    [setFieldValue]
  );

  return (
    <Fragment>
      <Col lg={100} md={100} sm={100}>
        <Text fw={8} mb={2} size={"medium"}>
          {t("group.scope.git.repo.credentials.title")}
        </Text>
      </Col>
      {_.isEmpty(groupedExistingCreds) ? null : (
        <Col lg={100} md={100} sm={100}>
          <Select
            label={t("group.scope.git.repo.credentials.existing")}
            name={"credentials.id"}
            onChange={onChangeExists}
          >
            <option value={""}>{""}</option>
            {Object.values(groupedExistingCreds).map(
              (cred): JSX.Element => (
                <option key={cred.id} value={cred.id}>
                  {cred.name}
                </option>
              )
            )}
          </Select>
        </Col>
      )}
      <Col lg={50} md={50} sm={50}>
        <Select
          disabled={true}
          fw={"bold"}
          label={t("group.scope.git.repo.credentials.type.text")}
          name={"credentials.typeCredential"}
          // eslint-disable-next-line
          onChange={onTypeChange} // NOSONAR
          required={!isEditing}
          tooltip={t("group.scope.git.repo.credentials.type.toolTip")}
        >
          <option value={""}>{""}</option>
          <option value={"SSH"}>
            {t("group.scope.git.repo.credentials.ssh")}
          </option>
          <option value={"USER"}>
            {t("group.scope.git.repo.credentials.userHttps")}
          </option>
          <option value={"TOKEN"}>
            {t("group.scope.git.repo.credentials.azureToken")}
          </option>
          {disabledCredsEdit ? (
            <option value={"OAUTH"}>
              {t("group.scope.git.repo.credentials.oauth")}
            </option>
          ) : undefined}
        </Select>
      </Col>
      <Col lg={50} md={50} sm={50}>
        <Input
          disabled={disabledCredsEdit}
          fw={"bold"}
          label={t("group.scope.git.repo.credentials.name.text")}
          name={"credentials.name"}
          required={!isEditing}
          tooltip={t("group.scope.git.repo.credentials.name.toolTip")}
        />
      </Col>
      {_.isEmpty(repoUrl) &&
      _.isEmpty(values.credentials.typeCredential) ? undefined : (
        <CredentialsType credExists={credExists} values={values} />
      )}
      {!showGitAlert && validateGitMsg.message !== "" ? (
        <Alert
          onTimeOut={setShowGitAlert}
          variant={validateGitMsg.type as IAlertProps["variant"]}
        >
          {validateGitMsg.message}
        </Alert>
      ) : undefined}
    </Fragment>
  );
};

export { CredentialsSection };
