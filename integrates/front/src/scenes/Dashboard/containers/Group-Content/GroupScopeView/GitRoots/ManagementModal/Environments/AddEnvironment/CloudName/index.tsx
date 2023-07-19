import { useFormikContext } from "formik";
import React from "react";
import type { FC } from "react";

import type { IFormProps } from "../types";
import { Select } from "components/Input";
import { Col } from "components/Layout";

const CloudName: FC = (): JSX.Element => {
  const { values } = useFormikContext<IFormProps>();

  const CloudNameSelect: JSX.Element =
    values.urlType === "CLOUD" ? (
      <Col>
        <Select label={"Cloud Name"} name={"cloudName"} required={true}>
          <option value={""}>{""}</option>
          <option value={"AWS"}>{"AWS"}</option>
          <option value={"GCP"}>{"Google Cloud Platform"}</option>
          <option value={"AZURE"}>{"Azure"}</option>
        </Select>
      </Col>
    ) : (
      <div />
    );

  return CloudNameSelect;
};

export { CloudName };
