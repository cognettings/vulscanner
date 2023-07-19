import type { ArrayHelpers } from "formik";

import type { IIntegrationRepository } from "../../types";

interface IExclusionsProps {
  exclusionsArrayHelpersRef: React.MutableRefObject<ArrayHelpers | null>;
  repositories: Record<string, IIntegrationRepository>;
}

export type { IExclusionsProps };
