import type { FormikProps } from "formik";

import type { IFormValues } from "../../../../../types";

interface IUrlProps {
  credExists: boolean;
  form: React.RefObject<FormikProps<IFormValues>>;
  isEditing: boolean;
  manyRows: boolean;
  setCredExists: React.Dispatch<React.SetStateAction<boolean>>;
  setIsSameHealthCheck: React.Dispatch<React.SetStateAction<boolean>>;
  setRepoUrl: (value: React.SetStateAction<string>) => void;
}

export type { IUrlProps };
