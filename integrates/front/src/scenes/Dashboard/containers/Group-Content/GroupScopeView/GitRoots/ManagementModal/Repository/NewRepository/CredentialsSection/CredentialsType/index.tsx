import type { FC } from "react";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../../../../../../types";
import { Input, TextArea } from "components/Input";
import { Col } from "components/Layout";

interface ICredentialsTypeProps {
  credExists: boolean;
  values: IFormValues;
}

export const CredentialsType: FC<ICredentialsTypeProps> = ({
  credExists,
  values,
}: ICredentialsTypeProps): JSX.Element | null => {
  const { t } = useTranslation();

  if (values.credentials.type === "SSH" && !credExists) {
    return (
      <TextArea
        fw={"bold"}
        label={t("group.scope.git.repo.credentials.sshKey.text")}
        name={"credentials.key"}
        placeholder={t("group.scope.git.repo.credentials.sshHint")}
        required={true}
        tooltip={t("group.scope.git.repo.credentials.sshKey.toolTip")}
      />
    );
  } else if (values.credentials.type === "HTTPS" && !credExists) {
    return (
      <Fragment>
        {values.credentials.auth === "USER" ? (
          <Fragment>
            <Col lg={50} md={50} sm={50}>
              <Input
                fw={"bold"}
                label={t("group.scope.git.repo.credentials.user.text")}
                name={"credentials.user"}
                required={true}
                tooltip={t("group.scope.git.repo.credentials.user.toolTip")}
              />
            </Col>
            <Col lg={50} md={50} sm={50}>
              <Input
                fw={"bold"}
                label={t("group.scope.git.repo.credentials.password.text")}
                name={"credentials.password"}
                required={true}
                tooltip={t("group.scope.git.repo.credentials.password.toolTip")}
              />
            </Col>
          </Fragment>
        ) : undefined}
        {values.credentials.auth === "TOKEN" ? (
          <Fragment>
            <Col lg={50} md={50} sm={50}>
              <Input
                fw={"bold"}
                label={t("group.scope.git.repo.credentials.token.text")}
                name={"credentials.token"}
                required={true}
                tooltip={t("group.scope.git.repo.credentials.token.toolTip")}
              />
            </Col>
            {values.credentials.isPat ? (
              <Col lg={50} md={50} sm={50}>
                <Input
                  fw={"bold"}
                  label={t(
                    "group.scope.git.repo.credentials.azureOrganization.text"
                  )}
                  name={"credentials.azureOrganization"}
                  required={true}
                  tooltip={t(
                    "group.scope.git.repo.credentials.azureOrganization.toolTip"
                  )}
                />
              </Col>
            ) : undefined}
          </Fragment>
        ) : undefined}
      </Fragment>
    );
  }

  return null;
};
