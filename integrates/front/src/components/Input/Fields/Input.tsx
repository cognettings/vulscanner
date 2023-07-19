import { Field } from "formik";
import type { FC } from "react";
import React from "react";

import type { IInputProps } from "../Formik/FormikInput";
import { FormikInput } from "../Formik/FormikInput";

const Input: FC<IInputProps> = ({
  bgColor,
  childLeft,
  childRight,
  disabled = false,
  fw,
  id,
  label,
  list,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  onPaste,
  placeholder,
  required,
  suggestions,
  tooltip,
  type = "text",
  validate,
  value,
  variant = "solid",
}: Readonly<IInputProps>): JSX.Element => (
  <Field
    bgColor={bgColor}
    childLeft={childLeft}
    childRight={childRight}
    component={FormikInput}
    disabled={disabled}
    fw={fw}
    id={id}
    label={label}
    list={list}
    name={name}
    onBlur={onBlur}
    onChange={onChange}
    onFocus={onFocus}
    onKeyDown={onKeyDown}
    onPaste={onPaste}
    placeholder={placeholder}
    required={required}
    suggestions={suggestions}
    tooltip={tooltip}
    type={type}
    validate={validate}
    value={value}
    variant={variant}
  />
);

export { Input };
