import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IPhoneNumberProps } from "../Formik/FormikPhone";
import { FormikPhone } from "../Formik/FormikPhone";

const PhoneField: FC<IPhoneNumberProps> = ({
  disabled,
  id,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  validate,
  variant,
}: Readonly<IPhoneNumberProps>): JSX.Element => (
  <Field
    component={FormikPhone}
    disabled={disabled}
    id={id}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    placeholder={placeholder}
    required={required}
    tooltip={tooltip}
    validate={validate}
    variant={variant}
  />
);

export { PhoneField };
