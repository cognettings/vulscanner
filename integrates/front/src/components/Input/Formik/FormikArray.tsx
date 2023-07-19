/* eslint-disable react/require-default-props */
import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import type { FormikProps } from "formik";
import { isEmpty, isNil } from "lodash";
import React, { Fragment, useCallback, useEffect } from "react";

import type { IInputProps } from "./FormikInput";

import { Input } from "../Fields/Input";
import { Button } from "components/Button";
import { Label } from "components/Input/Label";
import { Col, Row } from "components/Layout";

interface IInputArrayProps
  extends Omit<IInputProps, "childLeft" | "childRight" | "type"> {
  addButtonText?: string;
  initEmpty?: boolean;
  initValue?: string;
  max?: number;
}
interface IInputArray extends IInputArrayProps {
  form: FormikProps<unknown>;
  push: (obj: unknown) => void;
  remove: <T>(index: number) => T | undefined;
}

export const FormikArray: React.FC<IInputArray> = ({
  addButtonText = "",
  disabled,
  fw,
  id,
  initEmpty = true,
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
  form,
  push,
  remove,
}: IInputArray): JSX.Element => {
  const addItem = useCallback((): void => {
    push(initValue);
  }, [initValue, push]);

  const removeItem = useCallback(
    (index: number): (() => void) =>
      (): void => {
        remove(index);
      },
    [remove]
  );

  const values = (form.values as Record<string, unknown>)[name] as string[];

  useEffect((): void => {
    if (!initEmpty && isEmpty(values)) {
      push(initValue);
    }
  }, [initEmpty, initValue, push, values]);

  return (
    <div>
      <Label fw={fw} htmlFor={id} required={required} tooltip={tooltip}>
        {label}
      </Label>
      <Row>
        {values.length > 0 ? (
          <Fragment>
            {values.map((_, index: number): JSX.Element => {
              const fieldName = `${name}[${index}]`;

              return (
                <Col key={fieldName} lg={80} md={80} sm={80}>
                  <Input
                    childRight={
                      (!initEmpty && values.length === 1) ||
                      disabled === true ? (
                        <div />
                      ) : (
                        <Button
                          icon={faTrashAlt}
                          onClick={removeItem(index)}
                          size={"sm"}
                        />
                      )
                    }
                    disabled={disabled}
                    name={fieldName}
                    onBlur={onBlur}
                    onChange={onChange}
                    onFocus={onFocus}
                    onKeyDown={onKeyDown}
                    placeholder={placeholder}
                    validate={validate}
                    variant={variant}
                  />
                </Col>
              );
            })}
          </Fragment>
        ) : undefined}
        {isNil(max) || values.length < max ? (
          <Col lg={20} md={20} sm={20}>
            {isEmpty(addButtonText) ? (
              <Button
                disabled={disabled}
                icon={faPlus}
                onClick={addItem}
                size={"md"}
              />
            ) : (
              <Button
                disabled={disabled}
                icon={faPlus}
                onClick={addItem}
                size={"md"}
              >
                {addButtonText}
              </Button>
            )}
          </Col>
        ) : undefined}
      </Row>
    </div>
  );
};

export type { IInputArrayProps };
