import type { TEnrollPages } from "../types";

interface IFastTrackDesktop {
  setPage: React.Dispatch<React.SetStateAction<TEnrollPages>>;
}

interface IFormValues {
  provider: string;
}

export type { IFastTrackDesktop, IFormValues };
