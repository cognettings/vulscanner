import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IRadioProps } from "../Formik/FormikRadioGroup";
import { FormikRadioGroup } from "../Formik/FormikRadioGroup";

const RadioGroup: FC<IRadioProps> = ({
  disabled,
  fw,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  options,
  required,
  tooltip,
  validate,
  value,
}: Readonly<IRadioProps>): JSX.Element => (
  <Field
    component={FormikRadioGroup}
    disabled={disabled}
    fw={fw}
    label={label}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    options={options}
    required={required}
    tooltip={tooltip}
    type={"radio"}
    validate={validate}
    value={value}
  />
);

export type { IRadioProps };
export { RadioGroup };
