import React from "react";
import { useTranslation } from "react-i18next";

import { Input } from "components/Input";
import { FormGroup } from "components/Input/styles";

const EntryPointField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <Input
        label={t("group.toe.inputs.addModal.fields.entryPoint")}
        name={"entryPoint"}
        type={"text"}
      />
    </FormGroup>
  );
};

export { EntryPointField };
