import React from "react";
import { useTranslation } from "react-i18next";

import { TextArea } from "components/Input";
import { FormGroup } from "components/Input/styles";

const FilenameField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <TextArea
        label={t("group.toe.lines.addModal.fields.filename")}
        name={"filename"}
      />
    </FormGroup>
  );
};

export { FilenameField };
