import React, { useState } from "react";

import type { IFilter } from "./types";

import { FormikNumber } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const NumberFilter = ({ id, label, onChange, value }: IFilter): JSX.Element => {
  const [numberValue, setNumberValue] = useState(value);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const eventValue = event.target.value;
    setNumberValue(eventValue);
    onChange({ id, value: eventValue });
  };

  return (
    <Row key={id}>
      <Col>
        <FormikNumber
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange,
            value: numberValue ?? "",
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={label}
          name={id}
        />
      </Col>
    </Row>
  );
};

export { NumberFilter };
