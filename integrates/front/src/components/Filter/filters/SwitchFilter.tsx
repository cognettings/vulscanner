import React, { useState } from "react";

import type { IFilter } from "./types";

import type { ISwitchOptions } from "../types";
import { Label } from "components/Input";
import { FormikSwitch } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const SwitchFilter = ({
  switchValues,
  id,
  label,
  onChange,
}: IFilter): JSX.Element => {
  const [checkedOptions, setCheckedOptions] = useState(switchValues);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { value } = event.target;
    const checkedValue = event.target.checked;
    const newValues = checkedOptions?.map((option): ISwitchOptions => {
      if (option.value === value) return { ...option, checked: checkedValue };

      return option;
    });
    setCheckedOptions(newValues);
    onChange({ id, switchValues: newValues });
  };

  return (
    <Row key={id}>
      <Label> {label} </Label>
      {checkedOptions?.map((option): JSX.Element => {
        return (
          <Col key={option.value}>
            <FormikSwitch
              field={{
                checked: option.checked,
                name: option.value,
                onBlur: (): void => undefined,
                onChange: handleChange,
                value: option.value,
              }}
              form={{ errors: {}, isSubmitting: false, touched: {} }}
              id={id}
              label={option.label}
              name={option.value}
              value={option.value}
            />
          </Col>
        );
      })}
    </Row>
  );
};

export { SwitchFilter };
