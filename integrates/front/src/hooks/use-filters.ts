import _ from "lodash";

import type {
  IFilter,
  IFilterComp,
  ISwitchOptions,
} from "components/Filter/types";

export const useFilters = <IData extends object>(
  data: IData[],
  filters: IFilter<IData>[]
): IData[] => {
  function handleTextSelectCases(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (
      filter.value === "" ||
      filter.value === undefined ||
      _.defaultTo(filter.isBackFilter, false)
    )
      return true;

    switch (filter.filterFn) {
      case "caseSensitive":
        return String(dataPoint[filter.key]) === filter.value;

      case "caseInsensitive":
        return (
          String(dataPoint[filter.key]).toLowerCase() ===
          filter.value.toLowerCase()
        );

      case "includesSensitive":
        return String(dataPoint[filter.key]).includes(filter.value);

      case "includesInArray": {
        const array: unknown[] = JSON.parse(
          JSON.stringify(dataPoint[filter.key])
        );

        return array.includes(filter.value);
      }

      case "includesInsensitive":
      default:
        return String(dataPoint[filter.key])
          .toLowerCase()
          .includes(filter.value.toLowerCase());
    }
  }

  function handleCheckCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (_.isUndefined(filter.switchValues)) return true;
    const value = String(dataPoint[filter.key]).toLowerCase();
    const checkedValue = filter.switchValues.find(
      (switchValue: ISwitchOptions): boolean =>
        switchValue.value.toLowerCase() === value
    );

    if (_.isUndefined(checkedValue) || _.isUndefined(checkedValue.checked))
      return true;

    return checkedValue.checked
      ? true
      : !value.includes(checkedValue.value.toLowerCase());
  }

  function handleCheckBoxesCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (_.isEmpty(filter.checkValues)) return true;

    return filter.checkValues?.includes(String(dataPoint[filter.key])) ?? true;
  }

  function handleNumberCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    return _.isEmpty(filter.value)
      ? true
      : String(dataPoint[filter.key]) === filter.value;
  }

  function handleNumberRangeCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (
      filter.numberRangeValues === undefined ||
      _.every(filter.numberRangeValues, _.isNil) ||
      _.defaultTo(filter.isBackFilter, false)
    )
      return true;

    const currentNumber = _.toNumber(dataPoint[filter.key]);
    const isHigher = _.isNil(filter.numberRangeValues[0])
      ? true
      : currentNumber >= filter.numberRangeValues[0];
    const isLower = _.isNil(filter.numberRangeValues[1])
      ? true
      : currentNumber <= filter.numberRangeValues[1];

    return isLower && isHigher;
  }

  function handleDateRangeCase(
    dataPoint: IData,
    filter: IFilterComp<IData>
  ): boolean {
    if (filter.rangeValues === undefined) return true;
    const currentDate = Date.parse(String(dataPoint[filter.key]));
    const isHigher = _.isEmpty(filter.rangeValues[0])
      ? true
      : currentDate >= Date.parse(filter.rangeValues[0]);
    const isLower = _.isEmpty(filter.rangeValues[1])
      ? true
      : currentDate <= Date.parse(filter.rangeValues[1]);

    return isHigher && isLower;
  }

  function checkAllFilters(dataPoint: IData): boolean {
    return filters.every((filter): boolean => {
      if (typeof filter.key === "function")
        return filter.key(dataPoint, filter.value, filter.rangeValues);
      switch (filter.type) {
        case "number":
          return handleNumberCase(dataPoint, filter as IFilterComp<IData>);

        case "numberRange":
          return handleNumberRangeCase(dataPoint, filter as IFilterComp<IData>);

        case "dateRange":
          return handleDateRangeCase(dataPoint, filter as IFilterComp<IData>);

        case "checkBoxes":
          return handleCheckBoxesCase(dataPoint, filter as IFilterComp<IData>);

        case "switch":
          return handleCheckCase(dataPoint, filter as IFilterComp<IData>);

        case "text":
        case "select":
        default:
          return handleTextSelectCases(dataPoint, filter as IFilterComp<IData>);
      }
    });
  }

  return data.filter((entry: IData): boolean => checkAllFilters(entry));
};
