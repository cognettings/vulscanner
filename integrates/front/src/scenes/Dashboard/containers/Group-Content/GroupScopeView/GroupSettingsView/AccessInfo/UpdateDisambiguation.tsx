import MDEditor from "@uiw/react-md-editor";
import { ErrorMessage } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IFieldProps } from "./GroupContextForm";

import { Alert } from "components/Alert";
import { ValidationError } from "components/Input/styles";

export const UpdateDisambiguation: React.FC<IFieldProps> = ({
  field,
  form: { values, setFieldValue },
}: IFieldProps): JSX.Element => {
  const { t } = useTranslation();

  const handleMDChange = useCallback(
    (value: string | undefined): void => {
      setFieldValue("disambiguation", value);
    },
    [setFieldValue]
  );

  return (
    <React.Fragment>
      <MDEditor
        height={200}
        highlightEnable={false}
        onChange={handleMDChange}
        value={values.disambiguation}
      />
      <ValidationError>
        <ErrorMessage name={field.name} />
      </ValidationError>
      <Alert>
        {"*"}&nbsp;
        {t("searchFindings.groupAccessInfoSection.markdownAlert")}
      </Alert>
    </React.Fragment>
  );
};
