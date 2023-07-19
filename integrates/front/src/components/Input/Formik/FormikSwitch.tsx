import type { FC } from "react";
import React from "react";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { Switch } from "components/Switch";

interface ISwitchProps extends IInputBase<HTMLInputElement> {
  label?: { on: string; off: string };
  value?: string;
}

type TSwitchProps = ISwitchProps & TFieldProps;

const FormikSwitch: FC<TSwitchProps> = ({
  disabled,
  field: { checked, name, onBlur: fieldBlur, onChange: fieldChange },
  form,
  id,
  label,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  required,
  tooltip,
  value,
}: Readonly<TSwitchProps>): JSX.Element => {
  const [handleBlur, handleChange] = useHandlers(
    { onBlur: fieldBlur, onChange: fieldChange },
    { onBlur, onChange }
  );

  return (
    <InputBase
      form={form}
      id={id}
      label={
        <Switch
          checked={checked ?? false}
          disabled={disabled}
          label={label}
          name={name}
          onBlur={handleBlur}
          onChange={handleChange}
          onFocus={onFocus}
          onKeyDown={onKeyDown}
          value={value}
        />
      }
      name={name}
      required={required}
      tooltip={tooltip}
    />
  );
};

export type { ISwitchProps };
export { FormikSwitch };
