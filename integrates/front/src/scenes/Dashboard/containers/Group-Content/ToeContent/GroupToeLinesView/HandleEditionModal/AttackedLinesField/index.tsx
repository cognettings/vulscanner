import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import type { IAttackedLinesFieldProps } from "./types";

import { InputNumber, Label } from "components/Input";
import { FormGroup } from "components/Input/styles";

const AttackedLinesField: React.FC<IAttackedLinesFieldProps> =
  (): JSX.Element => {
    const { t } = useTranslation();

    const handleKeyDown = useCallback(
      (event: React.KeyboardEvent<HTMLInputElement>): void => {
        if (event.key.length > 1 || /\d/u.test(event.key)) return;
        event.preventDefault();
      },
      []
    );

    return (
      <FormGroup>
        <Label>
          <b>{t("group.toe.lines.editModal.fields.attackedLines")}</b>&nbsp;
          <i>
            {`(${t("group.toe.lines.editModal.fields.attackedLinesComment")})`}
          </i>
        </Label>
        <InputNumber min={0} name={"attackedLines"} onKeyDown={handleKeyDown} />
      </FormGroup>
    );
  };

export { AttackedLinesField };
