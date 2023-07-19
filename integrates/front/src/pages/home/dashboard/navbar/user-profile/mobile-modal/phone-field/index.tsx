import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IPhoneFieldProps } from "./types";

import { Label } from "components/Input";
import { PhoneField as Phone } from "components/Input/Fields/PhoneField";
import { FormGroup } from "components/Input/styles";
import {
  composeValidators,
  isValidPhoneNumber,
  required,
} from "utils/validations";

const PhoneField: React.FC<IPhoneFieldProps> = ({
  autoFocus,
  disabled,
  label,
  name,
}): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <Label>
        <b>
          {t(
            _.isUndefined(label)
              ? "profile.mobileModal.fields.phoneNumber"
              : label
          )}
        </b>
      </Label>
      <Phone
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={autoFocus}
        disabled={disabled}
        name={_.isUndefined(name) ? "phone" : name}
        validate={composeValidators([required, isValidPhoneNumber])}
      />
    </FormGroup>
  );
};

export { PhoneField };
