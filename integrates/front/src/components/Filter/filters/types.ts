/* eslint @typescript-eslint/no-explicit-any:0 */
import type {
  IPermanentData,
  ISelectedOptions,
  ISwitchOptions,
} from "../types";

interface IFilter {
  id: string;
  label: string;
  onChange: (permanentData: IPermanentData) => void;
  switchValues?: ISwitchOptions[];
  checkValues?: string[];
  mappedOptions?: ISelectedOptions[];
  minMaxRangeValues?: [number, number];
  numberRangeValues?: [number | undefined, number | undefined];
  rangeValues?: [string, string];
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

export type { IFilter };
