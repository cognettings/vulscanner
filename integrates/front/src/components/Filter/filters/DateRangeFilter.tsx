import dayjs from "dayjs";
import _ from "lodash";
import React, { useState } from "react";

import type { IFilter } from "./types";

import { FormikDate } from "components/Input/Formik";
import { Col, Row } from "components/Layout";

const DateRangeFilter = ({
  id,
  label,
  onChange,
  rangeValues,
}: IFilter): JSX.Element => {
  const [localRangeValues, setLocalRangeValues] = useState(
    _.isUndefined(rangeValues)
      ? undefined
      : [
          _.isEmpty(rangeValues[0])
            ? ""
            : dayjs(rangeValues[0]).format("YYYY-MM-DD"),
          _.isEmpty(rangeValues[1])
            ? ""
            : dayjs(rangeValues[1]).format("YYYY-MM-DD"),
        ]
  );

  const formatIsoDate = (
    dateString: string,
    toDate: boolean = false
  ): string => {
    if (_.isEmpty(dateString)) {
      return "";
    }
    const date = dayjs(dateString);

    if (toDate) {
      return date.endOf("day").toISOString();
    }

    return date.toISOString();
  };

  const handleChange = (
    position: 0 | 1
  ): ((event: React.ChangeEvent<HTMLInputElement>) => void) => {
    return (event: React.ChangeEvent<HTMLInputElement>): void => {
      const value: [string, string] =
        position === 0
          ? [event.target.value, localRangeValues?.[1] ?? ""]
          : [localRangeValues?.[0] ?? "", event.target.value];
      setLocalRangeValues(value);

      onChange({
        id,
        rangeValues: [formatIsoDate(value[0]), formatIsoDate(value[1], true)],
      });
    };
  };

  return (
    <Row key={id}>
      <Col lg={50} md={50}>
        <FormikDate
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(0),
            value: localRangeValues?.[0] ?? "",
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={label}
          name={id}
        />
      </Col>
      <Col lg={50} md={50}>
        <FormikDate
          field={{
            name: id,
            onBlur: (): void => undefined,
            onChange: handleChange(1),
            value: localRangeValues?.[1] ?? "",
          }}
          form={{ errors: {}, isSubmitting: false, touched: {} }}
          label={"\n"}
          name={id}
        />
      </Col>
    </Row>
  );
};

export { DateRangeFilter };
