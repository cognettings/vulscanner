import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { ISwitchProps } from "../Formik/FormikSwitch";
import { FormikSwitch } from "../Formik/FormikSwitch";

const Switch: FC<ISwitchProps> = ({
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  validate,
  value,
}: Readonly<ISwitchProps>): JSX.Element => (
  <Field
    component={FormikSwitch}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    required={required}
    tooltip={tooltip}
    type={"switch"}
    validate={validate}
    value={value}
  />
);

export { Switch };
