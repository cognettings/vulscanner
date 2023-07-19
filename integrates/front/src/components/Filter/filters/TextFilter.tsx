/* eslint-disable react/require-default-props */
import _ from "lodash";
import React, { useEffect, useState } from "react";

import type { IFilter } from "./types";

import { FormikInput } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const TextFilter = ({ id, label, onChange, value }: IFilter): JSX.Element => {
  const [textValue, setTextValue] = useState(value);
  const [hasInitialValue, setHasInitialValue] = useState(_.isEmpty(value));

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const eventValue = event.target.value;
    setTextValue(eventValue);
    onChange({ id, value: eventValue });
  };

  useEffect((): void => {
    if (!hasInitialValue) {
      onChange({ id, value });
      setHasInitialValue(!hasInitialValue);
    }
  }, [id, hasInitialValue, onChange, value]);

  return (
    <Row key={id}>
      <Col>
        <FormikInput
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange,
            value: textValue ?? "",
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={label}
          name={id}
        />
      </Col>
    </Row>
  );
};

export { TextFilter };
