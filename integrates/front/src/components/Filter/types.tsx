import type { Dispatch, SetStateAction } from "react";

interface IFilter<IData extends object> {
  checkValues?: string[];
  filterFn?:
    | "caseInsensitive"
    | "caseSensitive"
    | "includesInArray"
    | "includesInsensitive"
    | "includesSensitive";
  id: string;
  isBackFilter?: boolean;
  key:
    | keyof IData
    | ((
        arg0: IData,
        value?: string,
        rangeValues?: [string, string]
      ) => boolean);
  label: string;
  minMaxRangeValues?: [number, number];
  numberRangeValues?: [number | undefined, number | undefined];
  rangeValues?: [string, string];
  selectOptions?:
    | ISelectedOptions[]
    | string[]
    | ((arg0: IData[]) => ISelectedOptions[])
    | ((arg0: IData[]) => string[]);
  switchValues?: ISwitchOptions[];
  type?:
    | "checkBoxes"
    | "dateRange"
    | "number"
    | "numberRange"
    | "select"
    | "switch"
    | "text";
  value?: string;
}

interface ISelectedOptions {
  header: string;
  value: string;
}

interface ISwitchOptions {
  label: { on: string; off: string };
  value: string;
  checked?: boolean;
}

interface IFilterComp<IData extends object> extends IFilter<IData> {
  key: keyof IData;
}

interface IPermanentData {
  switchValues?: ISwitchOptions[];
  checkValues?: string[];
  id: string;
  value?: string;
  rangeValues?: [string, string];
  numberRangeValues?: [number | undefined, number | undefined];
}

interface IPermanentValuesProps {
  permaValue: IPermanentData;
  permaValues: IPermanentData[];
  setPermaValues?: Dispatch<SetStateAction<IPermanentData[]>>;
}

interface IFiltersProps<IData extends object> {
  dataset?: IData[];
  permaset?: [IPermanentData[], Dispatch<SetStateAction<IPermanentData[]>>];
  filters: IFilter<IData>[];
  setFilters: Dispatch<SetStateAction<IFilter<IData>[]>>;
}

export type {
  IFilter,
  IFilterComp,
  IFiltersProps,
  IPermanentData,
  IPermanentValuesProps,
  ISelectedOptions,
  ISwitchOptions,
};
