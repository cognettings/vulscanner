/* eslint react/forbid-component-props: 0 */
import type {
  ButtonHTMLAttributes,
  FC,
  MouseEventHandler,
  ReactElement,
  ReactNode,
} from "react";
import React, { useMemo } from "react";
import { IconContext } from "react-icons";
import type { IconType } from "react-icons";

import { StyledButton } from "./styledComponents";
import type { IStyledButtonProps } from "./types";

import { Container } from "../Container";

interface IButtonProps
  extends IStyledButtonProps,
    ButtonHTMLAttributes<HTMLButtonElement> {
  children?: ReactNode;
  icon?: ReactElement<IconType>;
  iconSide?: "left" | "right";
  onClick?: MouseEventHandler<HTMLButtonElement>;
}

const Button: FC<IButtonProps> = ({
  customSize,
  children,
  className,
  disabled,
  display,
  icon,
  iconSide = "left",
  name,
  onClick,
  selected,
  size,
  type,
  variant,
}: Readonly<IButtonProps>): JSX.Element => {
  const valueIconL = useMemo((): { className: string | undefined } => {
    return { className: children === undefined ? undefined : "mr1" };
  }, [children]);

  const valueIconR = useMemo((): { className: string | undefined } => {
    return { className: children === undefined ? undefined : "ml1" };
  }, [children]);

  return (
    <StyledButton
      className={className}
      customSize={customSize}
      disabled={disabled}
      display={display}
      name={name}
      onClick={onClick}
      selected={selected}
      size={size}
      type={type}
      variant={variant}
    >
      <Container
        align={"center"}
        display={"flex"}
        justify={display === "block" ? "center" : "unset"}
      >
        {iconSide === "left" ? (
          <IconContext.Provider value={valueIconL}>
            {icon ? icon : undefined}
            {children}
          </IconContext.Provider>
        ) : (
          <IconContext.Provider value={valueIconR}>
            {children}
            {icon ? icon : undefined}
          </IconContext.Provider>
        )}
      </Container>
    </StyledButton>
  );
};

export type { IButtonProps };
export { Button };
