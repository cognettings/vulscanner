import { faSearch } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useRef } from "react";
import styled from "styled-components";

import type { IInputBase, TFieldProps } from "../InputBase";
import { InputBase, useHandlers } from "../InputBase";
import { StyledInput } from "../styles";
import { createEvent } from "../utils";
import { Button } from "components/Button";

interface IInputFileProps extends IInputBase<HTMLInputElement> {
  accept?: string;
  multiple?: boolean;
}

type TInputFileProps = IInputFileProps & TFieldProps;

const FileInput = styled(StyledInput)`
  opacity: 0;
  position: absolute;
  visibility: hidden;
  width: 0;
`;

const SelectFile = styled.span`
  min-width: 100px;
`;

const getFileName = (value: unknown): string => {
  const files = value as FileList | undefined;

  if (files) {
    return Array.from(files)
      .map((file): string => file.name)
      .join(", ");
  }

  return "";
};

const FormikFile: React.FC<TInputFileProps> = ({
  accept,
  disabled = false,
  field: { name, onBlur: fieldBlur, onChange: fieldChange, value },
  form,
  id,
  label,
  multiple = false,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  variant = "solid",
}: Readonly<TInputFileProps>): JSX.Element => {
  const fileName = getFileName(value);

  const inputRef = useRef<HTMLInputElement>(null);

  const [handleBlur, handleChange] = useHandlers(
    { onBlur: fieldBlur, onChange: fieldChange },
    { onBlur, onChange }
  );

  const handleInputClick = useCallback((): void => {
    if (inputRef.current) {
      const changeEvent = createEvent("change", name, undefined);

      handleChange?.(
        changeEvent as unknown as React.ChangeEvent<HTMLInputElement>
      );
      // eslint-disable-next-line fp/no-mutation
      inputRef.current.value = "";
    }
  }, [name, handleChange]);

  const handleInputChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>): void => {
      const { files } = event.currentTarget;
      const changeEvent = createEvent(
        "change",
        name,
        files && files.length > 0 ? files : undefined
      );

      handleChange?.(
        changeEvent as unknown as React.ChangeEvent<HTMLInputElement>
      );
    },
    [name, handleChange]
  );

  const handleButtonClick = useCallback((): void => {
    if (inputRef.current) {
      inputRef.current.click();
    }
  }, []);

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
      <span className={"w-100"}>{fileName}</span>
      <FileInput
        accept={accept}
        aria-label={name}
        data-testid={name}
        disabled={disabled}
        id={id}
        multiple={multiple}
        name={name}
        onBlur={handleBlur}
        onChange={handleInputChange}
        onClick={handleInputClick}
        onFocus={onFocus}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        ref={inputRef}
        type={"file"}
      />
      <SelectFile>
        <Button
          disabled={disabled}
          icon={faSearch}
          onClick={handleButtonClick}
          size={"sm"}
          variant={"primary"}
        >
          {"Explore\u2026"}
        </Button>
      </SelectFile>
    </InputBase>
  );
};

export type { IInputFileProps };
export { FormikFile };
