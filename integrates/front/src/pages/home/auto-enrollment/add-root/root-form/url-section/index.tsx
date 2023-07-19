import { useFormikContext } from "formik";
import type { ChangeEvent, FC } from "react";
import React, { Fragment, useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IUrlProps } from "./types";

import type { IRootAttr } from "../../../types";
import { chooseCredentialType } from "../../utils";
import { Input } from "components/Input";
import { Col } from "components/Layout";
import { composeValidators, validTextField } from "utils/validations";

const UrlSection: FC<IUrlProps> = ({
  accessChecked,
  setRepoUrl,
}): JSX.Element => {
  const { t } = useTranslation();
  const { setFieldValue } = useFormikContext<IRootAttr>();

  const onChangeUrl = useCallback(
    (event: ChangeEvent<HTMLInputElement>): void => {
      const urlValue = event.target.value;
      setRepoUrl(urlValue);
      chooseCredentialType(urlValue, setFieldValue);
    },
    [setFieldValue, setRepoUrl]
  );

  return (
    <Fragment>
      <Col lg={50} md={50} sm={50}>
        <Input
          disabled={accessChecked}
          fw={"bold"}
          id={"git-root-add-repo-url"}
          label={t("autoenrollment.url.label")}
          name={"url"}
          onChange={onChangeUrl}
          placeholder={t("autoenrollment.url.placeHolder")}
          required={true}
          tooltip={t("autoenrollment.url.toolTip")}
          type={"text"}
          validate={composeValidators([validTextField])}
        />
      </Col>
      <Col id={"git-root-add-repo-branch"} lg={50} md={50} sm={50}>
        <Input
          disabled={accessChecked}
          fw={"bold"}
          label={t("autoenrollment.branch.label")}
          name={"branch"}
          required={true}
          tooltip={t("autoenrollment.branch.toolTip")}
        />
      </Col>
    </Fragment>
  );
};

export { UrlSection };
