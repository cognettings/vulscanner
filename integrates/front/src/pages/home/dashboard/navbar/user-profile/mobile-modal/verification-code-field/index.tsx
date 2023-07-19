import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IVerificationCodeFieldProps } from "./types";

import { Input } from "components/Input";
import { FormGroup } from "components/Input/styles";

const VerificationCodeField: React.FC<IVerificationCodeFieldProps> = ({
  disabled,
  name,
}): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <Input
        disabled={disabled}
        label={t("profile.mobileModal.fields.verificationCode")}
        name={_.isUndefined(name) ? "verificationCode" : name}
        type={"text"}
      />
    </FormGroup>
  );
};

export { VerificationCodeField };
