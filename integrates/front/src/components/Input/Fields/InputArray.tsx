import { FieldArray } from "formik";
import type { FC, ReactNode } from "react";
import React from "react";

import { FormikArray } from "../Formik/FormikArray";
import type { IInputArrayProps } from "../Formik/FormikArray";

const InputArray: FC<IInputArrayProps> = ({
  addButtonText,
  disabled,
  fw,
  id,
  initEmpty,
  initValue = "",
  label,
  max = undefined,
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
}: Readonly<IInputArrayProps>): JSX.Element => {
  return (
    <FieldArray name={name}>
      {({ form, push, remove }): ReactNode => {
        return (
          <FormikArray
            addButtonText={addButtonText}
            disabled={disabled}
            form={form}
            fw={fw}
            id={id}
            initEmpty={initEmpty}
            initValue={initValue}
            label={label}
            max={max}
            name={name}
            onBlur={onBlur}
            onChange={onChange}
            onFocus={onFocus}
            onKeyDown={onKeyDown}
            placeholder={placeholder}
            push={push}
            remove={remove}
            required={required}
            tooltip={tooltip}
            validate={validate}
            variant={variant}
          />
        );
      }}
    </FieldArray>
  );
};

export { InputArray };
