import React, { useState } from "react";

import type { IFilter } from "./types";

import { FormikSelect } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const SelectFilter = ({
  id,
  label,
  mappedOptions = [],
  onChange,
  value = "",
}: IFilter): JSX.Element => {
  const [selectValue, setSelectValue] = useState(value);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const eventValue = event.target.value;
    setSelectValue(eventValue);
    onChange({ id, value: eventValue });
  };

  return (
    <Row key={id}>
      <Col>
        <FormikSelect
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange,
            value: selectValue,
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={label}
          name={id}
        >
          <option value={""}>{"All"}</option>
          {mappedOptions.map((option): JSX.Element => {
            return (
              <option key={option.value} value={option.value}>
                {option.header}
              </option>
            );
          })}
        </FormikSelect>
      </Col>
    </Row>
  );
};

export { SelectFilter };
