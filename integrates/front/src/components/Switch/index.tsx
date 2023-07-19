import React, { useCallback } from "react";

import { Container, Slider } from "./styles";

interface ISwitchProps<T = HTMLInputElement> {
  checked: boolean;
  disabled?: boolean;
  label?: { on: string; off: string };
  name?: string;
  onBlur?: (event: React.FocusEvent<T>) => void;
  onChange?: (event: React.ChangeEvent<T>) => void;
  onFocus?: (event: React.FocusEvent<T>) => void;
  onKeyDown?: (event: React.KeyboardEvent<T>) => void;
  value?: string;
}

const Switch: React.FC<ISwitchProps> = ({
  checked,
  disabled,
  label,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  value,
}: Readonly<ISwitchProps>): JSX.Element => {
  // Disable click propagation in favor of the input onChange event
  const handleClick = useCallback(
    (event: React.MouseEvent<HTMLLabelElement>): void => {
      event.stopPropagation();
    },
    []
  );
  const longLength = 3;
  const longLabel =
    label !== undefined &&
    (label.on.length > longLength || label.off.length > longLength);
  const shortLabel = label !== undefined && !longLabel;

  return (
    <React.Fragment>
      {longLabel ? <span>{label[checked ? "on" : "off"]}</span> : undefined}
      <Container onClick={handleClick}>
        <input
          aria-label={name}
          checked={checked}
          disabled={disabled}
          name={name}
          onBlur={onBlur}
          onChange={onChange}
          onFocus={onFocus}
          onKeyDown={onKeyDown}
          type={"checkbox"}
          value={value}
        />
        <Slider>
          {shortLabel ? (
            <span>{label[checked ? "on" : "off"]}</span>
          ) : undefined}
        </Slider>
      </Container>
    </React.Fragment>
  );
};

export type { ISwitchProps };
export { Switch };
