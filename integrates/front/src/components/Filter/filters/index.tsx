import React from "react";

import { CheckBoxFilter } from "./CheckBoxFilter";
import { DateRangeFilter } from "./DateRangeFilter";
import { NumberFilter } from "./NumberFilter";
import { NumberRangeFilter } from "./NumberRangeFilter";
import { SelectFilter } from "./SelectFilter";
import { SwitchFilter } from "./SwitchFilter";
import { TextFilter } from "./TextFilter";
import type { IFilter as IFilterProps } from "./types";

const Filter = ({
  id,
  label,
  onChange,
  checkValues,
  mappedOptions,
  minMaxRangeValues,
  numberRangeValues,
  rangeValues,
  switchValues,
  type,
  value,
}: IFilterProps): JSX.Element => {
  switch (type) {
    case "text": {
      return (
        <TextFilter id={id} label={label} onChange={onChange} value={value} />
      );
    }
    case "number": {
      return (
        <NumberFilter id={id} label={label} onChange={onChange} value={value} />
      );
    }
    case "numberRange": {
      return (
        <NumberRangeFilter
          id={id}
          label={label}
          minMaxRangeValues={minMaxRangeValues}
          numberRangeValues={numberRangeValues}
          onChange={onChange}
        />
      );
    }
    case "select": {
      return (
        <SelectFilter
          id={id}
          label={label}
          mappedOptions={mappedOptions}
          onChange={onChange}
          value={value}
        />
      );
    }
    case "dateRange": {
      return (
        <DateRangeFilter
          id={id}
          label={label}
          onChange={onChange}
          rangeValues={rangeValues}
        />
      );
    }
    case "checkBoxes": {
      return (
        <CheckBoxFilter
          checkValues={checkValues}
          id={id}
          label={label}
          mappedOptions={mappedOptions}
          onChange={onChange}
        />
      );
    }
    case "switch": {
      return (
        <SwitchFilter
          id={id}
          label={label}
          onChange={onChange}
          switchValues={switchValues}
          value={value}
        />
      );
    }
    default: {
      return <div key={id} />;
    }
  }
};

export {
  CheckBoxFilter,
  DateRangeFilter,
  Filter,
  NumberFilter,
  NumberRangeFilter,
  SelectFilter,
  TextFilter,
};
