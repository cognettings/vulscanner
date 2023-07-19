import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { InputNumber } from "components/Input";
import { FormGroup } from "components/Input/styles";

const LinesOfCodeField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const handleKeyDown = useCallback(
    (event: React.KeyboardEvent<HTMLInputElement>): void => {
      if (
        event.key.length > 1 ||
        /\d/u.test(event.key) ||
        event.key === "Control" ||
        event.key.toLocaleLowerCase() === "v"
      )
        return;
      event.preventDefault();
    },
    []
  );

  return (
    <FormGroup>
      <InputNumber
        label={t("group.toe.lines.addModal.fields.loc")}
        min={0}
        name={"loc"}
        onKeyDown={handleKeyDown}
      />
    </FormGroup>
  );
};

export { LinesOfCodeField };
