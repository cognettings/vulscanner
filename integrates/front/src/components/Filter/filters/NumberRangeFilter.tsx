import _ from "lodash";
import React from "react";

import type { IFilter } from "./types";

import { FormikNumber } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const NumberRangeFilter = ({
  id,
  label,
  onChange,
  minMaxRangeValues,
  numberRangeValues,
}: IFilter): JSX.Element => {
  const handleChange = (
    position: 0 | 1
  ): ((event: React.ChangeEvent<HTMLInputElement>) => void) => {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      const targetValue = _.isEmpty(event.target.value)
        ? undefined
        : _.toNumber(event.target.value);
      const value: [number | undefined, number | undefined] =
        position === 0
          ? [targetValue, numberRangeValues?.[1]]
          : [numberRangeValues?.[0], targetValue];
      onChange({ id, numberRangeValues: value });
    };
  };

  return (
    <Row key={id}>
      <Col lg={50} md={50}>
        <FormikNumber
          enableTextLimit={true}
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(0),
            value: numberRangeValues?.[0]?.toString() ?? "",
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={label}
          max={minMaxRangeValues?.[1]}
          min={minMaxRangeValues?.[0]}
          name={id}
          placeholder={"Min"}
        />
      </Col>
      <Col lg={50} md={50}>
        <FormikNumber
          enableTextLimit={true}
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(1),
            value: numberRangeValues?.[1]?.toString() ?? "",
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={"\n"}
          max={minMaxRangeValues?.[1]}
          min={minMaxRangeValues?.[0]}
          name={id}
          placeholder={"Max"}
        />
      </Col>
    </Row>
  );
};

export { NumberRangeFilter };
