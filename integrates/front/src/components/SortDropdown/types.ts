interface ISelectedOptions {
  value: string;
  header: string;
}

interface ISortDropdown {
  id: string;
  onChange: (value: string, order: "ASC" | "DESC") => void;
  mappedOptions?: ISelectedOptions[];
}

export type { ISelectedOptions, ISortDropdown };
