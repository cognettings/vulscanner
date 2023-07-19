import type { FC } from "react";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import type { IRootAttr } from "../../../../types";
import { Input, TextArea } from "components/Input";
import { Col } from "components/Layout";

interface ICredentialsTypeProps {
  accessChecked: boolean;
  values: IRootAttr;
}

export const CredentialsType: FC<ICredentialsTypeProps> = ({
  accessChecked,
  values,
}: ICredentialsTypeProps): JSX.Element | null => {
  const { t } = useTranslation();

  if (values.credentials.type === "SSH") {
    return (
      <TextArea
        disabled={accessChecked}
        fw={"bold"}
        label={t("autoenrollment.credentials.sshKey.label")}
        name={"credentials.key"}
        placeholder={t("autoenrollment.credentials.sshKey.hint")}
        required={true}
        tooltip={t("autoenrollment.credentials.sshKey.toolTip")}
      />
    );
  } else if (values.credentials.type === "HTTPS") {
    return (
      <Fragment>
        {values.credentials.auth === "USER" ? (
          <Fragment>
            <Col lg={50} md={50} sm={50}>
              <Input
                disabled={accessChecked}
                fw={"bold"}
                label={t("autoenrollment.credentials.user.label")}
                name={"credentials.user"}
                required={true}
                tooltip={t("autoenrollment.credentials.user.toolTip")}
              />
            </Col>
            <Col lg={50} md={50} sm={50}>
              <Input
                disabled={accessChecked}
                fw={"bold"}
                label={t("autoenrollment.credentials.password.label")}
                name={"credentials.password"}
                required={true}
                tooltip={t("autoenrollment.credentials.password.toolTip")}
              />
            </Col>
          </Fragment>
        ) : undefined}
        {values.credentials.auth === "TOKEN" ? (
          <Fragment>
            <Col lg={50} md={50} sm={50}>
              <Input
                disabled={accessChecked}
                fw={"bold"}
                label={t("autoenrollment.credentials.token.label")}
                name={"credentials.token"}
                required={true}
                tooltip={t("autoenrollment.credentials.token.toolTip")}
              />
            </Col>
            {values.credentials.isPat ? (
              <Col lg={50} md={50} sm={50}>
                <Input
                  disabled={accessChecked}
                  fw={"bold"}
                  label={t(
                    "autoenrollment.credentials.azureOrganization.label"
                  )}
                  name={"credentials.azureOrganization"}
                  required={true}
                  tooltip={t(
                    "autoenrollment.credentials.azureOrganization.toolTip"
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
