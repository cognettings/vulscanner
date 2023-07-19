import React, { useCallback } from "react";

import { SwitcherButton, SwitcherWrapper } from "./styledComponents";

interface ISwitchProps {
  options: string[];
  state: number;
  setState: React.Dispatch<React.SetStateAction<number>>;
}

const Switch: React.FC<ISwitchProps> = ({
  options,
  state,
  setState,
}): JSX.Element => {
  const activeIndex = state;

  const handleSwitch = useCallback(
    (index: number): (() => void) =>
      (): void => {
        setState(index);
      },
    [setState]
  );

  return (
    <SwitcherWrapper>
      {options.map(
        (el: string, index: number): JSX.Element => (
          <SwitcherButton
            active={activeIndex === index}
            key={el}
            onClick={handleSwitch(index)}
          >
            {el}
          </SwitcherButton>
        )
      )}
    </SwitcherWrapper>
  );
};

export { Switch };
