import React from "react";
import { useTranslation } from "react-i18next";

import { Input } from "components/Input";
import { FormGroup } from "components/Input/styles";

const LastCommitField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <Input
        label={t("group.toe.lines.addModal.fields.lastCommit")}
        name={"lastCommit"}
        type={"text"}
      />
    </FormGroup>
  );
};

export { LastCommitField };
