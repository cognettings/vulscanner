import React, { useState } from "react";

import type { IFilter } from "./types";

import { Label } from "components/Input";
import { FormikCheckbox } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const CheckBoxFilter = ({
  checkValues = [],
  id,
  label,
  mappedOptions,
  onChange,
}: IFilter): JSX.Element => {
  const [checkBoxValues, setCheckBoxValues] = useState(checkValues);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const { value } = event.target;
    const isChecked = event.target.checked;
    const newValues = isChecked
      ? [...checkBoxValues, value]
      : checkBoxValues.filter((option): boolean => option !== value);
    setCheckBoxValues(newValues);
    onChange({ checkValues: newValues, id });
  };

  return (
    <Row key={id}>
      <Label> {label} </Label>
      {mappedOptions?.map((option): JSX.Element => {
        return (
          <Col key={option.value}>
            <FormikCheckbox
              field={{
                checked: checkBoxValues.includes(option.value),
                name: option.value,
                onBlur: (): void => undefined,
                onChange: handleChange,
                value: option.value,
              }}
              form={{ errors: {}, isSubmitting: false, touched: {} }}
              label={option.header}
              name={option.value}
              value={option.value}
            />
          </Col>
        );
      })}
    </Row>
  );
};

export { CheckBoxFilter };
