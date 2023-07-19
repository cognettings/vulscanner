import type { FormikProps } from "formik";
import type { Dispatch, SetStateAction } from "react";

import type { IFormValues } from "../../../../../types";

interface IHealthCheckProps {
  form: React.RefObject<FormikProps<IFormValues>>;
  isEditing: boolean;
  isSameHealthCheck: boolean;
  setIsSameHealthCheck: Dispatch<SetStateAction<boolean>>;
}

export type { IHealthCheckProps };
