import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { Select } from "components/Input";
import { Col } from "components/Layout";

const EnvironmentType: FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Col>
      <Select
        label={t("group.scope.git.addEnvironment.type")}
        name={"urlType"}
        required={true}
      >
        <option value={""}>{""}</option>
        <option value={"CLOUD"}>{"Cloud"}</option>
        <option value={"APK"}>{"Mobile App"}</option>
        <option value={"URL"}>{"URL"}</option>
      </Select>
    </Col>
  );
};

export { EnvironmentType };
