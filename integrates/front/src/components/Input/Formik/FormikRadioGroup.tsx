import type { FC } from "react";
import React from "react";
import styled from "styled-components";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { Text } from "components/Text";

interface IRadioGroupOption {
  checked?: boolean;
  header: string;
  value: string;
}
interface IRadioProps extends IInputBase<HTMLInputElement> {
  options: IRadioGroupOption[];
  value: string;
}

type TRadioProps = IRadioProps & TFieldProps;

const Radio = styled.input.attrs({
  type: `radio`,
})`
  -webkit-appearance: none;
  appearance: none;

  width: 13px;
  height: 13px;
  border: 1px solid #dddde3;
  border-radius: 50%;
  margin-right: 2px;

  display: grid;
  place-content: center;
  cursor: pointer;

  :disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  ::before {
    content: "";
    width: 9px;
    height: 9px;
    border-radius: 50%;
    transform: scale(0);
    transition: 120ms transform ease-in-out;
    box-shadow: inset 1em 1em #2e2e38;
  }

  :checked {
    border: 1px solid #2e2e38;
  }

  :checked::before {
    transform: scale(1);
  }
`;

const RadioBox = styled.label`
  cursor: pointer;
  display: flex;
  align-items: center;
`;

// Id must be unique for radio groups to work properly
const getDefaultId = (name: string, value: unknown): string => {
  if (typeof value === "boolean") {
    return name;
  }

  return [name, value].join("-");
};

const FormikRadioGroup: FC<TRadioProps> = ({
  disabled,
  field: { name, onBlur: fieldBlur, onChange: fieldChange, value },
  form,
  fw,
  id = getDefaultId(name, value),
  label,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  options,
  required,
  tooltip,
}: Readonly<TRadioProps>): JSX.Element => {
  const [handleBlur, handleChange] = useHandlers(
    { onBlur: fieldBlur, onChange: fieldChange },
    { onBlur, onChange }
  );

  return (
    <InputBase
      form={form}
      fw={fw}
      id={id}
      label={label}
      name={name}
      required={required}
      tooltip={tooltip}
      variant={"outline"}
    >
      {options.map((option: IRadioGroupOption): JSX.Element => {
        return (
          <RadioBox id={getDefaultId(name, option.value)} key={option.value}>
            <Radio
              checked={value === option.value}
              disabled={disabled}
              name={name}
              onBlur={handleBlur}
              onChange={handleChange}
              onFocus={onFocus}
              onKeyDown={onKeyDown}
              value={option.value}
            />
            <div>
              <Text bright={7} mr={2} tone={"dark"}>
                {option.header}
              </Text>
            </div>
          </RadioBox>
        );
      })}
    </InputBase>
  );
};

export type { IRadioProps };
export { FormikRadioGroup };
