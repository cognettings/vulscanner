import { useFormikContext } from "formik";
import _ from "lodash";
import React, { Fragment, useCallback } from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { CredentialsType } from "./credentials-type";
import type { ICredentialsType } from "./types";

import type { IRootAttr } from "../../../types";
import { Input, Select } from "components/Input";
import { Col } from "components/Layout";
import { Text } from "components/Text";

const CredentialsSection: FC<ICredentialsType> = ({
  accessChecked,
  repoUrl,
}): JSX.Element => {
  const { t } = useTranslation();
  const { setFieldValue, values } = useFormikContext<IRootAttr>();

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
          {t("autoenrollment.credentials.title")}
        </Text>
      </Col>
      <Col lg={50} md={50} sm={50}>
        <Select
          disabled={true}
          fw={"bold"}
          label={t("autoenrollment.credentials.type.label")}
          name={"credentials.typeCredential"}
          // eslint-disable-next-line
          onChange={onTypeChange}
          required={true}
          tooltip={t("autoenrollment.credentials.type.toolTip")}
        >
          <option value={""}>{""}</option>
          <option value={"SSH"}>{t("autoenrollment.credentials.ssh")}</option>
          <option value={"USER"}>
            {t("autoenrollment.credentials.userHttps")}
          </option>
          <option value={"TOKEN"}>
            {t("autoenrollment.credentials.azureToken")}
          </option>
        </Select>
      </Col>
      <Col lg={50} md={50} sm={50}>
        <Input
          disabled={accessChecked}
          fw={"bold"}
          label={t("autoenrollment.credentials.name.label")}
          name={"credentials.name"}
          required={true}
          tooltip={t("autoenrollment.credentials.name.toolTip")}
        />
      </Col>
      {_.isEmpty(repoUrl) &&
      _.isEmpty(values.credentials.typeCredential) ? undefined : (
        <CredentialsType accessChecked={accessChecked} values={values} />
      )}
    </Fragment>
  );
};

export { CredentialsSection };
