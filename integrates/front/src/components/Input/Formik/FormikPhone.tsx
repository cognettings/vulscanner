import _ from "lodash";
import type { FC, FocusEvent } from "react";
import React, { useCallback } from "react";
import type { CountryData } from "react-phone-input-2";
import PhoneInput from "react-phone-input-2";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase } from "../InputBase";
import { createEvent } from "../utils";

import "react-phone-input-2/lib/bootstrap.css";

interface IPhoneNumberProps extends IInputBase<HTMLInputElement> {
  autoFocus?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

type TInputPhoneProps = IPhoneNumberProps & TFieldProps;

const FormikPhone: FC<TInputPhoneProps> = ({
  disabled = false,
  field: { name, onBlur: onBlurField, onChange, value },
  form,
  id,
  label,
  onBlur,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  variant = "solid",
}: Readonly<TInputPhoneProps>): JSX.Element => {
  const onPhoneChange = useCallback(
    (
      currentNumber: string,
      countryData: CountryData,
      _event: React.ChangeEvent<HTMLInputElement>,
      _formattedValue: string
    ): void => {
      const info = {
        callingCountryCode: countryData.dialCode,
        countryCode: countryData.countryCode,
        nationalNumber: currentNumber.substring(
          _.isUndefined(countryData.dialCode) ? 0 : countryData.dialCode.length
        ),
      };

      const changeEvent = createEvent("change", name, info);

      onChange(changeEvent);
    },
    [name, onChange]
  );

  const handleBlur = useCallback(
    (ev: FocusEvent<HTMLInputElement>): void => {
      onBlurField(ev);
      onBlur?.(ev);
    },
    [onBlur, onBlurField]
  );

  return (
    <InputBase
      form={form}
      id={id}
      label={label}
      name={name}
      required={required}
      tooltip={tooltip}
      variant={variant}
    >
      <PhoneInput
        aria-label={name}
        country={_.get(value, "countryCode", undefined)}
        disableCountryGuess={true}
        disabled={disabled}
        inputProps={{
          autoFocus: onFocus,
          name,
        }}
        onBlur={handleBlur}
        onChange={onPhoneChange}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        preferredCountries={["co", "us"]}
        value={
          String(_.get(value, "callingCountryCode", "")) +
          String(_.get(value, "nationalNumber", ""))
        }
      />
    </InputBase>
  );
};

export type { IPhoneNumberProps };
export { FormikPhone };
