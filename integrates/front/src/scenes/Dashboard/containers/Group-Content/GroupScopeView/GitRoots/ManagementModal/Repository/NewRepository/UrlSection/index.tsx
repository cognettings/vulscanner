import { useFormikContext } from "formik";
import type { ChangeEvent, FC } from "react";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IUrlProps } from "./types";

import type { IFormValues } from "../../../../../types";
import { chooseCredentialType, updateHealthCheckConfirm } from "../utils";
import { Alert } from "components/Alert";
import { Checkbox, Input } from "components/Input";
import { Col } from "components/Layout";
import { composeValidators, validTextField } from "utils/validations";

const UrlSection: FC<IUrlProps> = ({
  credExists,
  form,
  isEditing,
  manyRows,
  setCredExists,
  setIsSameHealthCheck,
  setRepoUrl,
}): JSX.Element => {
  const { t } = useTranslation();
  const { initialValues, setFieldValue, values } =
    useFormikContext<IFormValues>();

  const onChangeUrl = useCallback(
    (event: ChangeEvent<HTMLInputElement>): void => {
      const urlValue = event.target.value;
      setRepoUrl(urlValue);
      chooseCredentialType(urlValue, credExists, setCredExists, setFieldValue);
      updateHealthCheckConfirm(
        form,
        initialValues,
        isEditing,
        setIsSameHealthCheck,
        urlValue
      );
    },
    [
      credExists,
      form,
      initialValues,
      isEditing,
      setCredExists,
      setFieldValue,
      setIsSameHealthCheck,
      setRepoUrl,
    ]
  );

  const onChangeBranch = useCallback(
    (event: ChangeEvent<HTMLInputElement>): void => {
      const branchValue = event.target.value;
      updateHealthCheckConfirm(
        form,
        initialValues,
        isEditing,
        setIsSameHealthCheck,
        undefined,
        branchValue
      );
    },
    [form, initialValues, isEditing, setIsSameHealthCheck]
  );

  return (
    <Fragment>
      {manyRows ? undefined : (
        <Col lg={50} md={50} sm={50}>
          <Input
            fw={"bold"}
            id={"git-root-add-repo-url"}
            label={t("group.scope.git.repo.url.text")}
            name={"url"}
            onChange={onChangeUrl}
            placeholder={t("group.scope.git.repo.url.placeHolder")}
            required={true}
            tooltip={t("group.scope.git.repo.url.toolTip")}
            type={"text"}
            validate={composeValidators([validTextField])}
          />
        </Col>
      )}
      <Col id={"git-root-add-repo-branch"} lg={50} md={50} sm={50}>
        <Input
          fw={"bold"}
          label={t("group.scope.git.repo.branch.text")}
          name={"branch"}
          onChange={onChangeBranch}
          required={true}
          tooltip={t("group.scope.git.repo.branch.toolTip")}
        />
      </Col>
      <Col id={"git-root-add-use-vpn"} lg={100} md={100} sm={100}>
        <Checkbox label={t("group.scope.git.repo.useVpn")} name={"useVpn"} />
      </Col>
      {isEditing && values.branch !== initialValues.branch ? (
        <Alert>{t("group.scope.common.changeWarning")}</Alert>
      ) : undefined}
    </Fragment>
  );
};

export { UrlSection };
