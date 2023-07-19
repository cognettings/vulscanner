import dayjs from "dayjs";
import _ from "lodash";

import type { ISelectedOptions, ISwitchOptions } from "../types";

function formatValue(
  value: string | undefined,
  mappedOptions: ISelectedOptions[] | undefined
): string | undefined {
  if (_.isEmpty(value)) {
    return undefined;
  }

  const formattedValue =
    mappedOptions === undefined
      ? value
      : mappedOptions.find((option): boolean => option.value === value)?.header;

  return formattedValue;
}

function formatCheckValues(
  checkValues: string[] | undefined,
  mappedOptions: ISelectedOptions[] | undefined
): string | undefined {
  if (_.isEmpty(checkValues)) {
    return undefined;
  }

  const formattedCheckValues =
    checkValues === undefined
      ? undefined
      : checkValues
          .map(
            (checkValue): string =>
              mappedOptions?.find(
                (option): boolean => option.value === checkValue
              )?.header ?? ""
          )
          .join(", ");

  return formattedCheckValues;
}

function formatNumberRange(
  rangeValues: [number | undefined, number | undefined] | undefined
): string | undefined {
  if (_.isUndefined(rangeValues) || _.every(rangeValues, _.isNil)) {
    return undefined;
  }
  if (!_.isNil(rangeValues[0]) && !_.isNil(rangeValues[1])) {
    return `${rangeValues[0]} - ${rangeValues[1]}`;
  }
  if (!_.isNil(rangeValues[0])) {
    return `Min ${rangeValues[0]}`;
  }
  if (!_.isNil(rangeValues[1])) {
    return `Max ${rangeValues[1]}`;
  }

  return undefined;
}

function formatDateRange(
  rangeValues: string[] | undefined
): string | undefined {
  if (rangeValues === undefined) {
    return undefined;
  }
  if (rangeValues[0] !== "" && rangeValues[1] !== "") {
    return `${dayjs(rangeValues[0]).format("LL")} - ${dayjs(
      rangeValues[1]
    ).format("LL")}`;
  }
  if (rangeValues[0] !== "") {
    return `From ${dayjs(rangeValues[0]).format("LL")}`;
  }
  if (rangeValues[1] !== "") {
    return `To ${dayjs(rangeValues[1]).format("LL")}`;
  }

  return undefined;
}

function formatSwitchValues(
  switchValues: ISwitchOptions[] | undefined
): string | undefined {
  if (_.isUndefined(switchValues)) {
    return undefined;
  }

  const formattedSwitchValues: ISwitchOptions[] = switchValues.filter(
    ({ checked }: ISwitchOptions): boolean => !_.isUndefined(checked) && checked
  );

  return _.isEmpty(formattedSwitchValues)
    ? undefined
    : formattedSwitchValues
        .map(({ label }: ISwitchOptions): string => label.on)
        .join(", ");
}

export {
  formatCheckValues,
  formatDateRange,
  formatNumberRange,
  formatSwitchValues,
  formatValue,
};
